from django.contrib import admin

# from haystack.admin import SearchModelAdmin
from .search_all_admin import SearchModelAdmin

from .models import (
    Query,
    AllIndex
)


# Register your models here.

class AllAdmin(SearchModelAdmin):
    search_fields = ('achar',)
    list_filter = ('achar', 'aint')
    list_display = ('achar', 'aint')

    def has_add_permission(self, request):
        return False


admin.site.register(Query)
admin.site.register(AllIndex, AllAdmin)
