import random

from django.contrib.sites.models import Site
from django.template import RequestContext

from cms.models import CMSPlugin, Title

from haystack import indexes

from djangocms_internalsearch.base import BaseSearchConfig
from djangocms_internalsearch.contrib.cms.filters import (
    AuthorFilter,
    SiteFilter,
    VersionStateFilter,
)
from djangocms_internalsearch.helpers import get_request


def get_title(obj):
    return obj.result.title


def get_slug(obj):
    return obj.result.slug


def get_site_name(obj):
    return obj.result.site_name


def get_language(obj):
    return obj.result.language


def get_author(obj):
    return obj.result.created_by


def get_content_type(obj):
    return obj.result.model.__name__


def get_version_status(obj):
    return obj.result.version_status


def get_modified_date(obj):
        return obj.result.creation_date


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
    list_display = [get_title, get_slug, get_content_type, get_site_name, get_language, get_author,
                    get_version_status, get_modified_date]
    list_filter = [SiteFilter, AuthorFilter, VersionStateFilter, ]
    search_fields = ('text', 'title')
    ordering = ('-id',)
    list_per_page = 50

    get_slug.short_description = 'slug'
    get_title.short_description = 'title'
    get_language.short_description = 'language'
    get_site_name.short_description = 'site_name'
    get_author.short_description = 'Author'
    get_content_type.short_description = 'Content Type'
    get_version_status.short_description = 'Version Status'
    get_modified_date.short_description = 'Modified Date'

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
