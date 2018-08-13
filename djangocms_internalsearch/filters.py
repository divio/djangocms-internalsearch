from django.contrib import admin

from cms.models.pagemodel import Page
from cms.models.titlemodels import Title


class LanguageFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'language'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'lang'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        languages = (
            Title.objects
            .order_by()
            .distinct()
            .values_list('language', flat=True)
        )
        return ((item, item) for item in languages)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() is not None:
            return queryset.filter(language=self.value())


class VersionStateFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'version state'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'version_state'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        # TODO: hard coding filter. Todo once versioning app ready.
        return (
            ('Archived', 'Archived'),
            ('Draft', 'Draft'),
            ('Published', 'Published'),
            ('Unpublished', 'Unpublished'),
            ('Locked', 'Locked'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is not None:
            return queryset.filter(version_status=self.value())


class AuthorFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'author'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'auth'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        authors = (
            Page.objects
            .order_by()
            .distinct()
            .values_list('changed_by', flat=True)
        )
        return ((item, item) for item in authors)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() is not None:
            return queryset.filter(created_by=self.value())
