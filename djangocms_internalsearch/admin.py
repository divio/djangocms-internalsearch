from django.contrib import admin
from .search_all_admin import SearchModelAdmin

from .models import (
    Query,
    QueryProxy
)


# Register your models here.

class AllAdmin(SearchModelAdmin):
    search_fields = ('achar',)
    #list_filter = ('achar', 'aint')
    list_display = ('achar', 'aint')


    def has_add_permission(self, request):
        return False

    def achar(self, obj):
        return obj.achar

    def aint(self, obj):
        return obj.aint


admin.site.register(Query)
admin.site.register(QueryProxy, AllAdmin)
