from django.contrib import admin

from djangocms_internalsearch.helpers import (
    get_internalsearch_config,
    get_model_class,
)


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

        model = get_model_class(self.value())
        if model:
            return queryset.models(model)
