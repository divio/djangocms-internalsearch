from django.contrib import admin
from .search_all_admin import SearchModelAdmin

from .models import (
    Query,
    QueryProxy
)


class DemoBoolFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Filter bools'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'abool'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('abooltrue', 'abool True'),
            ('aboolfalse', 'abool False'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        print('all {}'.format(queryset.count()))
        if self.value() == 'abooltrue':
            print('filter true {}'.format(queryset.filter(abool=1).count()))
            return queryset.filter(abool=1)
        if self.value() == 'aboolfalse':
            print('filter true {}'.format(queryset.filter(abool=0).count()))
            return queryset.filter(abool=0)


# Register your models here.

class AllAdmin(SearchModelAdmin):
    search_fields = ('achar',)
    list_filter = (DemoBoolFilter,)
    list_display = ('achar', 'aint')

    def has_add_permission(self, request):
        return False

    def achar(self, obj):
        return obj.achar

    def aint(self, obj):
        return obj.aint


admin.site.register(Query)
admin.site.register(QueryProxy, AllAdmin)
