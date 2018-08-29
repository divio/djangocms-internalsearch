from __future__ import print_function, unicode_literals

import operator
from functools import reduce

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import InvalidPage, Paginator
from django.db import models

from haystack.admin import SearchModelAdminMixin
from haystack.query import SearchQuerySet

from .models import InternalSearchProxy


class InternalSearchChangeList(ChangeList):
    def __init__(self, request, model, list_display, list_display_links,
                 list_filter, date_hierarchy, search_fields, list_select_related,
                 list_per_page, list_max_show_all, list_editable, model_admin):
        self.haystack_connection = 'default'
        super().__init__(request, model, list_display, list_display_links,
                         list_filter, date_hierarchy, search_fields, list_select_related,
                         list_per_page, list_max_show_all, list_editable, model_admin)

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
        self.full_result_count = full_result_count
        self.show_admin_actions = not self.show_full_result_count or bool(full_result_count)
        self.result_list = result_list
        self.can_show_all = can_show_all
        self.multi_page = multi_page
        self.paginator = paginator

    @staticmethod
    def _make_model(result):
        model = InternalSearchProxy(pk=result.pk)
        model.result = result
        model.app_label = result.model._meta.app_label
        model.model_name = result.model._meta.model_name
        return model


class InternalSearchQuerySet(SearchQuerySet):
    def __init__(self, using=None, query=None):
        super().__init__(using, query)
        self.query.select_related = False


class InternalSearchModelAdminMixin(SearchModelAdminMixin):

    def get_changelist(self, request, **kwargs):
        """
        Returns the ChangeList class for use on the changelist page.
        """
        return InternalSearchChangeList

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = InternalSearchQuerySet(self.haystack_connection).all()
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


@admin.register(InternalSearchProxy)
class InternalSearchAdmin(InternalSearchModelAdminMixin, ModelAdmin):
    # Todo: use model config to generate admin attributes and methods
    list_display = ['title', 'slug', 'content_type', 'language', 'author', 'version_status', 'modified_date']
    list_per_page = 50
    search_fields = ('text', 'title')
    ordering = ('-id',)
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def modified_date(selfs, obj):
        return obj.result.modified_date

    def slug(self, obj):
        return obj.result.slug

    def text(self, obj):
        return obj.text

    def title(self, obj):
        return obj.result.title

    def language(self, obj):
        return obj.result.language

    def site_name(self, obj):
        return obj.result.site_name

    def author(self, obj):
        return obj.result.created_by

    def content_type(self, obj):
        return obj.result.model.__name__

    def version_status(self, obj):
        return obj.result.version_status
