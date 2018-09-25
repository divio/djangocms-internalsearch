from django.apps import apps
from django.contrib import admin
from django.contrib.auth import get_user_model

from cms.models import Site
from cms.utils.i18n import get_language_list

from djangocms_internalsearch.helpers import get_internalsearch_config


class ContentTypeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Content type'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        models_meta = [
            (app.model._meta, app.model.__name__) for app in get_internalsearch_config()
        ]
        return (item for item in models_meta)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        # qs = super(InternalSearchAdmin, self).changelist(request, queryset)
        if not self.value():
            return

        model = apps.get_model(self.value())
        if model:
            return queryset.models(model)


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
        User = get_user_model()
        authors = User.objects.values_list('username', flat=True)
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
            return queryset.filter(version_author=self.value())


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
        return ((item, item) for item in get_language_list())

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
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
