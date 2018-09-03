import random

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.test import RequestFactory
from django.utils.html import format_html

from cms.models import CMSPlugin, Title
from cms.toolbar.toolbar import CMSToolbar

from filer.models.filemodels import File
from filer.models.imagemodels import Image
from haystack import indexes

from djangocms_internalsearch.base import BaseSearchConfig
from djangocms_internalsearch.contrib.cms.filters import (
    AuthorFilter,
    SiteFilter,
    VersionStateFilter,
)


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

    # admin setting
    list_display = ['title', 'slug', 'absolute_url', 'content_type', 'site_name', 'language', 'author',
                    'version_status', 'modified_date']
    list_filter = [SiteFilter, AuthorFilter, VersionStateFilter, ]
    search_fields = ('text', 'title')
    ordering = ('-id',)
    list_per_page = 15

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

    def modified_date(self, obj):
        return obj.result.modified_date

    def slug(self, obj):
        return obj.result.slug

    def absolute_url(self, obj):
        if obj.result.url:
            return format_html("<a href='{url}'>{url}</a>", url=obj.result.url)
        else:
            return obj.result.url

    absolute_url.short_description = 'URL'
    absolute_url.allow_tags = True

    def text(self, obj):
        return obj.text

    def title(self, obj):
        return obj.result.title

    def language(self, obj):
        return obj.result.language

    def site_name(self, obj):
        return obj.result.site_name

    def author(self, obj):
        return obj.result.created_by

    def content_type(self, obj):
        return obj.result.model.__name__

    def version_status(self, obj):
        return obj.result.version_status


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
    list_display = ['title', 'file_size', 'file_path_new']
    search_fields = ('title', 'folder_name')
    list_filter = ()

    model = File

    def title(self, obj):
        return obj.result.file_path

    def file_path_new(self, obj):
        return obj.result.file

    def file_size(self, obj):
        return obj.result.file_size

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
    list_display = ['title', 'file_path']
    search_fields = ('title', 'folder_name')
    list_filter = ()

    model = Image

    def file_path(self, obj):
        return obj.result.file

    def folder_name(self, obj):
        return obj.result.folder_name

    def prepare_text(self, obj):
        # Todo: Might need to change based on file type e.g. Image
        return ' '.join([obj.original_filename, ])
