import random

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.test import RequestFactory

from cms.models import CMSPlugin, Title
from cms.toolbar.toolbar import CMSToolbar

from haystack import indexes

from djangocms_internalsearch.base import BaseSearchConfig
from djangocms_internalsearch.contrib.cms.filters import AuthorFilter


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

    def prepare_site_id(self, obj):
        return obj.page.node.site_id

    def prepare_site_name(self, obj):
        site_id = obj.page.node.site_id
        return Site.objects.filter(pk=site_id).values_list('domain', flat=True)[0]

    def prepare_plugin_types(self, obj):
        plugin_types = (
            CMSPlugin
            .objects
            .filter(placeholder__title=obj.pk, language=obj.language)
            .order_by()  # Needed for distinct() with values_list https://code.djangoproject.com/ticket/16058
            .values_list('plugin_type', flat=True)
            .distinct()
        )
        return list(plugin_types)

    def prepare_text(self, obj):
        plugins = CMSPlugin.objects.filter(
            language=obj.language,
            placeholder__title=obj.id,
        )
        request = get_request(obj.language)
        context = RequestContext(request)
        renderer = request.toolbar.content_renderer
        rendered_plugins = []

        for base_plugin in plugins:
            plugin_content = renderer.render_plugin(
                instance=base_plugin,
                context=context,
                editable=False,
            )
            rendered_plugins.append(plugin_content)
        return ' '.join(rendered_plugins)

    def prepare_version_status(self, obj):
        # TODO: prepare from djangocms_versioning apps
        # Creating random for time being for UI Filter
        return random.choice(['Draft', 'Published', 'Unpublished', 'Archived', 'Locked'])

    def prepare_created_by(self, obj):
        return obj.page.changed_by

    # admin setting
    list_display = ['id', 'title', 'slug', 'site_name', 'language',
                    'author', 'content_type', 'version_status']

    list_filter = (AuthorFilter, )

    search_fields = ('text', 'title')
    list_per_page = 15
    ordering = ('-id',)


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
