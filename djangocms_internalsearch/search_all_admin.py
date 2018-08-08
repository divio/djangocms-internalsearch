# encoding: utf-8

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from django.contrib.admin.options import ModelAdmin, csrf_protect_m
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import SEARCH_VAR, ChangeList
from django.core.exceptions import PermissionDenied
from django.core.paginator import InvalidPage, Paginator
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ungettext

from haystack.query import SearchQuerySet
from haystack.utils import get_model_ct_tuple

from .models import QueryProxy


def list_max_show_all(changelist):
    """
    Returns the maximum amount of results a changelist can have for the
    "Show all" link to be displayed in a manner compatible with both Django
    1.4 and 1.3. See Django ticket #15997 for details.
    """
    try:
        # This import is available in Django 1.3 and below
        from django.contrib.admin.views.main import MAX_SHOW_ALL_ALLOWED
        return MAX_SHOW_ALL_ALLOWED
    except ImportError:
        return changelist.list_max_show_all


class SearchChangeList(ChangeList):
    def __init__(self, **kwargs):
        self.haystack_connection = kwargs.pop('haystack_connection', 'default')
        super(SearchChangeList, self).__init__(**kwargs)

    def get_results(self, request):
        sqs = self.queryset
        if SEARCH_VAR in request.GET:
            sqs = sqs.auto_query(request.GET[SEARCH_VAR]).load_all()

        paginator = Paginator(sqs, self.list_per_page)
        # Get the number of objects, with admin filters applied.
        result_count = paginator.count
        full_result_count = SearchQuerySet(self.haystack_connection).all().count()

        can_show_all = result_count <= list_max_show_all(self)
        multi_page = result_count > self.list_per_page

        # Get the list of objects to display on this page.
        try:
            result_list = paginator.page(self.page_num + 1).object_list
            result_list = [SearchChangeList._make_model(result) for result in result_list]
        except InvalidPage:
            result_list = ()

        self.result_count = result_count
        self.full_result_count = full_result_count
        self.result_list = result_list
        self.can_show_all = can_show_all
        self.multi_page = multi_page
        self.paginator = paginator

    def get_ordering(self, request, queryset):
        return ['-id']

    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        url = reverse('admin:%s_%s_change' % (result.internal_search_result.app_label,
                                              result.internal_search_result.model_name),
                      args=(quote(pk),),
                      current_app=self.model_admin.admin_site.name)
        return url

    @staticmethod
    def _make_model(result):
        model = QueryProxy(pk=result.pk)
        # TODO DL this feels hacky, not sure if there is a better way
        model.internal_search_result = result
        return model


class SearchQuerySetInternalSearch(SearchQuerySet):
    def __init__(self, using=None, query=None):
        super().__init__(using, query)
        self.query.select_related = False

    def _clone(self, klass=None):
        clone = super()._clone(klass)
        clone.query.select_related = False
        return clone


class SearchModelAdminMixin(object):
    # haystack connection to use for searching
    haystack_connection = 'default'

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if not self.has_change_permission(request, None):
            raise PermissionDenied

        # # Do a search of just this model and populate a Changelist with the
        # # returned bits.
        # if not self.model in connections[self.haystack_connection].get_unified_index().get_indexed_models():
        #     # Oops. That model isn't being indexed. Return the usual
        #     # behavior instead.
        #     return super(SearchModelAdminMixin, self).changelist_view(request, extra_context)

        # So. Much. Boilerplate.
        # Why copy-paste a few lines when you can copy-paste TONS of lines?
        list_display = list(self.list_display)

        kwargs = {
            'haystack_connection': self.haystack_connection,
            'request': request,
            'model': self.model,
            'list_display': list_display,
            'list_display_links': self.list_display_links,
            'list_filter': self.list_filter,
            'date_hierarchy': self.date_hierarchy,
            'search_fields': self.search_fields,
            'list_select_related': self.list_select_related,
            'list_per_page': self.list_per_page,
            'list_editable': self.list_editable,
            'model_admin': self,
            # 'sortable_by': None, This might be needed in the next version of django
        }

        # Django 1.4 compatibility.
        if hasattr(self, 'list_max_show_all'):
            kwargs['list_max_show_all'] = self.list_max_show_all

        changelist = SearchChangeList(**kwargs)
        changelist.formset = None
        media = self.media

        # Build the action form and populate it with available actions.
        # Check actions to see if any are available on this changelist
        actions = self.get_actions(request)
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = self.get_action_choices(request)
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
            # More Django 1.4 compatibility
            'root_path': getattr(self.admin_site, 'root_path', None),
            'app_label': self.model._meta.app_label,
            'action_form': action_form,
            'actions_on_top': self.actions_on_top,
            'actions_on_bottom': self.actions_on_bottom,
            'actions_selection_counter': getattr(self, 'actions_selection_counter', 0),
            'opts': QueryProxy._meta
        }
        context.update(extra_context or {})
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
        qs = SearchQuerySetInternalSearch(self.haystack_connection).all()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_search_results(self, request, queryset, search_term):
        """Override the base class"""
        return queryset, False


class SearchModelAdmin(SearchModelAdminMixin, ModelAdmin):
    pass
