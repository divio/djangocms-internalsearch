import random

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.test import RequestFactory

from cms.models import CMSPlugin, Placeholder, Title
from cms.toolbar.toolbar import CMSToolbar

from haystack import indexes

from .base import BaseSearchConfig
from .helpers import render_plugin


class PageContentConfig(BaseSearchConfig):
    """
    Page config and index definition
    """
    page = indexes.IntegerField(model_attr='page__id')
    title = indexes.CharField(model_attr='title')
    slug = indexes.CharField(model_attr='slug')
    site_id = indexes.IntegerField()
    site_name = indexes.CharField()
    language = indexes.CharField(model_attr='language')
    plugin_types = indexes.MultiValueField()
    created_by = indexes.CharField()
    version_status = indexes.CharField()
    creation_date = indexes.DateTimeField(model_attr='creation_date')

    # model class attribute
    model = Title

    # admin setting
    list_display = ('page_title', 'language', 'version_status', 'changed_by')
    list_filter = ('language', 'site_name', 'changed_by',)

    def prepare_site_id(self, obj):
        return obj.page.node.site_id

    def prepare_site_name(self, obj):
        site_id = obj.page.node.site_id
        return Site.objects.filter(pk=site_id).first().domain

    def prepare_plugin_types(self, obj):
        placeholder_ids = (
            placeholder.pk for placeholder in Placeholder.objects.filter(title=obj.id)
        )
        plugin_types = [
            plugin.plugin_type for plugin in
            CMSPlugin.objects.filter(placeholder__in=placeholder_ids)
        ]
        # Returning unique CMS Plugin types
        return set(plugin_types)

    def prepare_text(self, obj):
        rendered_text = []
        language = obj.language
        placeholder_ids = (
            placeholder.pk for placeholder in Placeholder.objects.filter(title=obj.id)
        )
        plugins = CMSPlugin.objects.filter(placeholder__in=placeholder_ids, language=language)
        request = get_request(language)
        context = RequestContext(request)
        renderer = request.toolbar.content_renderer
        for base_plugin in plugins:
            rendered_text.append(render_plugin(base_plugin, context, renderer))

        return rendered_text

    def prepare_version_status(self, obj):
        # TODO: prepare from djangocms_versioning apps
        # Creating random for time being for UI Filter
        return random.choice(['Draft', 'Published', 'Unpublished', 'Archived', 'Locked'])

    def prepare_created_by(self, obj):
        return obj.page.changed_by


def get_request(language=None):
    """
    Returns a Request instance populated with cms specific attributes.
    """
    request_factory = RequestFactory(HTTP_HOST=settings.ALLOWED_HOSTS[0])
    request = request_factory.get("/")
    request.session = {}
    request.LANGUAGE_CODE = language or settings.LANGUAGE_CODE
    # Needed for plugin rendering.
    request.current_page = None
    request.user = AnonymousUser()
    request.toolbar = CMSToolbar(request)
    return request
