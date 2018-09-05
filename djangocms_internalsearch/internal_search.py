import random

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.test import RequestFactory

from cms.models import CMSPlugin, PageContent, PageUrl
from cms.toolbar.toolbar import CMSToolbar

from filer.models.filemodels import File
from filer.models.imagemodels import Image
from haystack import indexes

from .base import BaseSearchConfig


class PageContentConfig(BaseSearchConfig):
    """
    Page config and index definition
    """
    page = indexes.IntegerField(model_attr='page__id')
    title = indexes.CharField(model_attr='title')
    slug = indexes.CharField()
    site_id = indexes.IntegerField()
    site_name = indexes.CharField()
    language = indexes.CharField(model_attr='language')
    plugin_types = indexes.MultiValueField()
    created_by = indexes.CharField()
    version_status = indexes.CharField()
    creation_date = indexes.DateTimeField(model_attr='creation_date')

    # admin setting
    list_display = ['id', 'title', 'slug', 'site_name', 'language',
                    'author', 'content_type', 'version_status']

    search_fields = ('text', 'title')
    ordering = ('-id',)

    # model class attribute
    model = PageContent

    def prepare_slug(self, obj):
        return PageUrl.objects.filter(pk=obj.page_id).first().slug

    def prepare_site_id(self, obj):
        return obj.page.node.site_id

    def prepare_site_name(self, obj):
        site_id = obj.page.node.site_id
        return Site.objects.filter(pk=site_id).values_list('domain', flat=True)[0]

    def prepare_plugin_types(self, obj):
        plugin_types = (
            CMSPlugin
            .objects
            .filter(placeholder_id=obj.pk, language=obj.language)
            .order_by()  # Needed for distinct() with values_list https://code.djangoproject.com/ticket/16058
            .values_list('plugin_type', flat=True)
            .distinct()
        )
        return list(plugin_types)

    def prepare_text(self, obj):
        plugins = CMSPlugin.objects.filter(
            language=obj.language,
            placeholder_id=obj.id,
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


class FilerFileConfig(BaseSearchConfig):
    # indexes definition
    folder_name = indexes.CharField(model_attr="folder__name")
    file_path = indexes.CharField(model_attr="file")
    title = indexes.CharField(model_attr="original_filename")
    file_size = indexes.IntegerField(model_attr="_file_size")
    created_by = indexes.CharField(model_attr="owner")
    version_status = indexes.CharField()

    # admin setting
    list_display = ['file_src', 'file_name', 'folder_name']
    search_fields = ('file_name', 'folder_name')

    model = File

    def prepare_text(self, obj):
        # Todo: Might need to change based on file type e.g. Image
        return ' '.join([obj.original_filename, ])


class FilerImageConfig(BaseSearchConfig):
    # indexes definition
    folder_name = indexes.CharField(model_attr="folder__name")
    file_path = indexes.CharField(model_attr="file")
    title = indexes.CharField(model_attr="original_filename")
    file_size = indexes.IntegerField(model_attr="_file_size")
    created_by = indexes.CharField(model_attr="owner")
    version_status = indexes.CharField()

    # admin setting
    list_display = ['file_src', 'file_name', 'folder_name']
    search_fields = ('file_name', 'folder_name')

    model = Image

    def prepare_text(self, obj):
        # Todo: Might need to change based on file type e.g. Image
        return ' '.join([obj.original_filename, ])
