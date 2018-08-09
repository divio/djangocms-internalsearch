from __future__ import absolute_import, division, print_function, unicode_literals

import operator
from functools import reduce

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin, csrf_protect_m
from django.contrib.admin.views.main import SEARCH_VAR, ChangeList
from django.contrib.admin.utils import quote
from django.core.exceptions import PermissionDenied
from django.core.paginator import InvalidPage, Paginator
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ungettext
from django.db import models

from haystack.query import SearchQuerySet
from haystack.utils import get_model_ct_tuple
from haystack.admin import SearchModelAdminMixin

from .models import InternalSearchProxy


class InternalSearchChangeList(ChangeList):
    def __init__(self, **kwargs):
        self.haystack_connection = kwargs.pop('haystack_connection', 'default')
        super(InternalSearchChangeList, self).__init__(**kwargs)

    def get_results(self, request):

        sqs = self.queryset
        if SEARCH_VAR in request.GET:
            sqs = sqs.auto_query(request.GET[SEARCH_VAR]).load_all()

        paginator = Paginator(sqs, self.list_per_page)

        # Get the number of objects, with admin filters applied.
        result_count = paginator.count
        full_result_count = SearchQuerySet(
            self.haystack_connection).models(self.model).all().count()

        can_show_all = result_count <= self.list_max_show_all
        multi_page = result_count > self.list_per_page

        # Get the list of objects to display on this page.
        try:
            result_list = paginator.page(self.page_num + 1).object_list
            # Grab just the Django models, since that's what everything else is
            # expecting.

            # result_list = [result.object for result in result_list]
            result_list = [InternalSearchChangeList._make_model(
                result) for result in result_list]

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
        url = reverse('admin:%s_%s_change' % (result.internal_search_app_label,
                                              result._internal_search_model_name),
                      args=(quote(pk),),
                      current_app=self.model_admin.admin_site.name)
        return url

    @staticmethod
    def _make_model(result):
        model = InternalSearchProxy(pk=result.pk)
        model.internal_search_app_label = result.model._meta.app_label
        model._internal_search_model_name = result.model._meta.model_name
        model.result = result
        return model


class SearchQuerySetInternalSearch(SearchQuerySet):
    def __init__(self, using=None, query=None):
        super().__init__(using, query)
        self.query.select_related = False

    def _clone(self, klass=None):
        clone = super()._clone(klass)
        clone.query.select_related = False
        return clone


class InternalSearchModelAdminMixin(SearchModelAdminMixin):

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if not self.has_change_permission(request, None):
            raise PermissionDenied

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
            'list_max_show_all': self.list_max_show_all
            #'sortable_by': None, This might be needed in the next version of django
        }

        changelist = InternalSearchChangeList(**kwargs)
        formset = changelist.formset = None
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
            'root_path': getattr(self.admin_site, 'root_path', None),
            'app_label': self.model._meta.app_label,
            'action_form': action_form,
            'actions_on_top': self.actions_on_top,
            'actions_on_bottom': self.actions_on_bottom,
            'actions_selection_counter': getattr(self, 'actions_selection_counter', 0),
            'opts': InternalSearchProxy._meta
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
        """
        Returns a tuple containing a queryset to implement the search,
        and a boolean indicating if the results may contain duplicates.
        """
        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        use_distinct = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            orm_lookups = [construct_search(str(search_field))
                           for search_field in search_fields]
            for bit in search_term.split():
                or_queries = [models.Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))

        return queryset, False


class SearchModelAdmin(InternalSearchModelAdminMixin, ModelAdmin):
    pass

# class DemoBoolFilter(admin.SimpleListFilter):
# # Human-readable title which will be displayed in the
# # right admin sidebar just above the filter options.
#     title = 'Filter bools'
#
#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = 'abool'
#
#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         return (
#             ('abooltrue', 'abool True'),
#             ('aboolfalse', 'abool False'),
#         )
#
#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         # Compare the requested value (either '80s' or '90s')
#         # to decide how to filter the queryset.
#         print('all {}'.format(queryset.count()))
#         if self.value() == 'abooltrue':
#             print('filter true {}'.format(queryset.filter(abool=1).count()))
#             return queryset.filter(abool=1)
#         if self.value() == 'aboolfalse':
#             print('filter true {}'.format(queryset.filter(abool=0).count()))
#             return queryset.filter(abool=0)
#


@admin.register(InternalSearchProxy)
class IntenalSearchAdmin(SearchModelAdmin):
    search_fields = ('text',)
    # list_filter = (DemoBoolFilter,)
    list_display = ['title', 'site_name', 'language', 'author', 'content_type', 'version_state']

    def has_add_permission(self, request):
        return False

    def text(self, obj):
        return obj.text

    def language(self, obj):
        return obj.result.language

    def site_name(self, obj):
        return obj.result.site_name

    def title(self, obj):
        # import ipdb
        # ipdb.set_trace()
        return obj.result.title

    def author(self, obj):
        return obj.result.created_by

    def content_type(self, obj):
        return obj.result.content_type()

    def version_state(self, obj):
        return obj.result.version_status
    # def get_title(self, obj):
    #     return obj.title

    # def __getattr__(self, obj):
    #     if hasattr(obj, 'title'):
    #         return getattr(obj, 'title')
