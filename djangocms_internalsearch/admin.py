from __future__ import print_function, unicode_literals

import operator
from functools import reduce

from django.apps import apps
from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.admin.options import ModelAdmin, csrf_protect_m
from django.core.exceptions import PermissionDenied
from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _, ungettext

from haystack.admin import SearchChangeList, SearchModelAdminMixin
from haystack.query import SearchQuerySet
from haystack.utils import get_model_ct_tuple

from djangocms_internalsearch.internal_search import InternalSearchAdminSetting

from .filters import AuthorFilter, ContentTypeFilter, VersionStateFilter
from .helpers import get_internalsearch_model_config, get_moderated_models
from .models import InternalSearchProxy


try:
    from djangocms_moderation.admin_actions import add_items_to_collection
except ImportError:
    add_items_to_collection = None


class InternalSearchChangeList(SearchChangeList):

    def get_results(self, request):

        sqs = self.queryset
        if hasattr(request, 'SEARCH_VAR'):
            query = request.GET('SEARCH_VAR')
            if query:
                sqs = sqs.auto_query(query)

        paginator = Paginator(sqs, self.list_per_page)

        # Get the number of objects, with admin filters applied.
        result_count = paginator.count
        full_result_count = sqs.count()

        can_show_all = result_count <= self.list_max_show_all
        multi_page = result_count > self.list_per_page

        # Get the list of objects to display on this page.
        try:
            result_list = paginator.page(self.page_num + 1).object_list
            # Grab just the Django models, since that's what everything else is
            # expecting.
            result_list = [
                InternalSearchChangeList._make_model(result)
                for result in result_list
            ]
        except InvalidPage:
            result_list = ()

        self.result_count = result_count
        self.show_full_result_count = self.model_admin.show_full_result_count
        # Admin actions are shown if there is at least one entry
        # or if entries are not counted because show_full_result_count is disabled
        self.show_admin_actions = not self.show_full_result_count or bool(full_result_count)
        self.full_result_count = full_result_count
        self.result_list = result_list
        self.can_show_all = can_show_all
        self.multi_page = multi_page
        self.paginator = paginator

    @staticmethod
    def _make_model(result):
        model = InternalSearchProxy(pk=result.pk)
        model.haystack_id = result.id
        model.result = result
        model.app_label = result.model._meta.app_label
        model.model_name = result.model._meta.model_name
        return model


class InternalSearchQuerySet(SearchQuerySet):
    def __init__(self, using=None, query=None):
        super().__init__(using, query)
        self.query.select_related = False


def get_admin_settings_from_config(model_meta):
    result = {}
    model_class = apps.get_model(model_meta)
    if model_class:
        app_config = get_internalsearch_model_config(model_class)
        if app_config:
            result.update({
                'list_display': app_config.list_display,
                'list_filter': app_config.list_filter,
                # TODO: adept more settings
            })

    return result


class InternalSearchModelAdminMixin(SearchModelAdminMixin):

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if not self.has_change_permission(request, None):
            raise PermissionDenied

        list_filter = list(InternalSearchAdminSetting.list_filter)
        list_display = list(InternalSearchAdminSetting.list_display)

        model_meta = request.GET.get('type')
        if model_meta:
            config_setting = get_admin_settings_from_config(model_meta)
            for item in config_setting.get('list_filter'):
                if item not in list_filter:
                    list_filter.append(item)

            if config_setting.get('list_display'):
                list_display = config_setting.get('list_display')

        extra_context = {'title': 'Internal Search'}
        actions = self.get_actions(request)
        if actions:
            if model_meta:
                list_display = ['action_checkbox'] + list(list_display)
            else:
                list_display = ['action_checkbox_haystack'] + list(list_display)

        kwargs = {
            'haystack_connection': self.haystack_connection,
            'request': request,
            'model': self.model,
            'list_display': list_display,
            'list_display_links': self.list_display_links,
            'list_filter': list_filter,
            'date_hierarchy': self.date_hierarchy,
            'search_fields': self.search_fields,
            'list_select_related': self.list_select_related,
            'list_per_page': self.list_per_page,
            'list_editable': self.list_editable,
            'model_admin': self,
            'list_max_show_all': self.list_max_show_all,
        }

        changelist = InternalSearchChangeList(**kwargs)
        changelist.formset = None
        media = self.media

        # If the request was POSTed, this might be a bulk action or a bulk
        # edit. Try to look up an action or confirmation first, but if this
        # isn't an action the POST will fall through to the bulk edit check,
        # below.
        action_failed = False
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        # Actions with no confirmation
        if (actions and request.method == 'POST' and 'index' in request.POST and '_save' not in request.POST):
            if selected:
                response = self.response_action(request, queryset=changelist.get_queryset(request))
                if response:
                    return response
                else:
                    action_failed = True
            else:
                msg = _("Items must be selected in order to perform "
                        "actions on them. No items have been changed.")
                self.message_user(request, msg, messages.WARNING)
                action_failed = True

        # Actions with confirmation
        if (actions and request.method == 'POST' and helpers.ACTION_CHECKBOX_NAME in request.POST and
                'index' not in request.POST and '_save' not in request.POST):
            if selected:
                response = self.response_action(request, queryset=changelist.get_queryset(request))
                if response:
                    return response
                else:
                    action_failed = True

        if action_failed:
            # Redirect back to the changelist page to avoid resubmitting the
            # form if the user refreshes the browser or uses the "No, take
            # me back" button on the action confirmation page.
            return HttpResponseRedirect(request.get_full_path())

        # Build the action form and populate it with available actions.
        # Check actions to see if any are available on this changelist
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = self.get_action_choices(request)
            media += action_form.media
        else:
            action_form = None

        selection_note = ungettext('0 of %(count)d selected',
                                   'of %(count)d selected', len(changelist.result_list))
        selection_note_all = ungettext('%(total_count)s selected',
                                       'All %(total_count)s selected', changelist.result_count)

        context = {
            'module_name': force_text(self.model._meta.verbose_name_plural),
            'selection_note': selection_note % {'count': len(changelist.result_list)},
            'selection_note_all': selection_note_all % {'total_count': changelist.result_count},
            'title': changelist.title,
            'is_popup': changelist.is_popup,
            'cl': changelist,
            'media': media,
            'has_add_permission': self.has_add_permission(request),
            'root_path': getattr(self.admin_site, 'root_path', None),
            'app_label': self.model._meta.app_label,
            'action_form': action_form,
            'actions_on_top': self.actions_on_top,
            'actions_on_bottom': self.actions_on_bottom,
            'actions_selection_counter': getattr(self, 'actions_selection_counter', 0),
            'opts': InternalSearchProxy._meta,

        }
        if extra_context:
            context.update(extra_context)

        request.current_app = self.admin_site.name
        app_name, model_name = get_model_ct_tuple(self.model)
        return render(request, self.change_list_template or [
            'admin/%s/%s/change_list.html' % (app_name, model_name),
            'admin/%s/change_list.html' % app_name,
            'admin/change_list.html'
        ], context)

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        model_meta = request.GET.get('type')
        qs = InternalSearchQuerySet(self.haystack_connection).all()
        if model_meta:
            model_klass = apps.get_model(model_meta)
            qs = InternalSearchQuerySet(self.haystack_connection).models(model_klass).all()

            # TODO: this should be handled by some parameter to the ChangeList.
            ordering = self.get_ordering(request)
            if ordering:
                qs = qs.order_by(*ordering)
        return qs

    def get_search_results(self, request, queryset, search_term):
        """
        Returns a tuple containing a queryset to implement the search,
        and a boolean indicating if the results may contain duplicates.
        """

        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            orm_lookups = [construct_search(str(search_field))
                           for search_field in search_fields]
            for bit in search_term.split():
                or_queries = [models.Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))

        return queryset, False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']

        model_meta = request.GET.get('type')
        if not model_meta or apps.get_model(model_meta) in get_moderated_models():
            if add_items_to_collection:
                actions['djangocms_moderation'] = (
                    add_items_to_collection, 'djangocms_moderation', add_items_to_collection.short_description)

        return actions

    def action_checkbox_haystack(self, obj):
        """
        A list_display column containing a checkbox widget.
        """
        return helpers.checkbox.render(helpers.ACTION_CHECKBOX_NAME, str(obj.haystack_id))

    action_checkbox_haystack.short_description = mark_safe('<input type="checkbox" id="action-toggle">')

    def action_checkbox(self, obj):
        """
        A list_display column containing a checkbox widget.
        """
        return helpers.checkbox.render(helpers.ACTION_CHECKBOX_NAME, str(obj.pk))

    action_checkbox.short_description = mark_safe('<input type="checkbox" id="action-toggle">')

    def response_action(self, request, queryset):
        """
        Handle an admin action. This is called if a request is POSTed to the
        changelist; it returns an HttpResponse if the action was handled, and
        None otherwise.
        """

        # There can be multiple action forms on the page (at the top
        # and bottom of the change list, for example). Get the action
        # whose button was pushed.
        try:
            action_index = int(request.POST.get('index', 0))
        except ValueError:
            action_index = 0

        # Construct the action form.
        data = request.POST.copy()
        data.pop(helpers.ACTION_CHECKBOX_NAME, None)
        data.pop("index", None)

        # Use the action whose button was pushed
        try:
            data.update({'action': data.getlist('action')[action_index]})
        except IndexError:
            # If we didn't get an action from the chosen form that's invalid
            # POST data, so by deleting action it'll fail the validation check
            # below. So no need to do anything here
            pass

        action_form = self.action_form(data, auto_id=None)
        action_form.fields['action'].choices = self.get_action_choices(request)

        # If the form's valid we can handle the action.
        if action_form.is_valid():
            action = action_form.cleaned_data['action']
            select_across = action_form.cleaned_data['select_across']
            func = self.get_actions(request)[action][0]

            # Get the list of selected PKs. If nothing's selected, we can't
            # perform an action on it, so bail. Except we want to perform
            # the action explicitly on all objects.
            selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
            if not selected and not select_across:
                # Reminder that something needs to be selected or nothing will happen
                msg = _("Items must be selected in order to perform "
                        "actions on them. No items have been changed.")
                self.message_user(request, msg, messages.WARNING)
                return None

            if not select_across:
                # Perform the action only on the selected objects
                model_meta = request.GET.get('type')
                if model_meta:
                    queryset = queryset.filter(pk__in=selected)
                else:
                    queryset = queryset.filter(id__in=selected)

            response = func(self, request, queryset)

            # Actions may return an HttpResponse-like object, which will be
            # used as the response from the POST. If not, we'll be a good
            # little HTTP citizen and redirect back to the changelist page.
            if isinstance(response, HttpResponseBase):
                return response
            else:
                return HttpResponseRedirect(request.get_full_path())
        else:
            msg = _("No action selected.")
            self.message_user(request, msg, messages.WARNING)
            return None


@admin.register(InternalSearchProxy)
class InternalSearchAdmin(InternalSearchModelAdminMixin, ModelAdmin, InternalSearchAdminSetting):
    list_display = ['title', 'slug', 'absolute_url', 'published_url', 'content_type', 'site_name', 'language', 'author',
                    'version_status', 'modified_date']
    list_filter = [ContentTypeFilter, AuthorFilter, VersionStateFilter, ]
    list_per_page = 50
    search_fields = ('text', 'title')
    ordering = ('-id',)
    list_display_links = None

    def has_add_permission(self, request):
        return False
