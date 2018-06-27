from django.contrib import admin
from .models import InternalSearch


@admin.register(InternalSearch)
class InternalSearchAdmin(admin.ModelAdmin):
    pass
