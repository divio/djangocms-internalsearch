from django.contrib import admin
from django.contrib.sites.models import Site

from cms.models import PageContent


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
            PageContent
            .objects
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


class SiteFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Site'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'site'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        sites = (
            Site
            .objects
            .order_by()
            .distinct()
            .values_list('name', flat=True)
        )
        return ((item, item) for item in sites)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() is not None:
            return queryset.filter(site_name=self.value())
