from django.contrib import admin
from django.db import models
from cms.extensions import PageExtensionAdmin
from cms.extensions.extension_pool import extension_pool
from cms.extensions.models import PageExtension
from .models import InternalSearch


class InternalSearchAdmin(admin.ModelAdmin):
    pass


admin.site.register(InternalSearch, InternalSearchAdmin)
