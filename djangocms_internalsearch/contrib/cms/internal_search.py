import random

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin, PageContent
from cms.toolbar.utils import get_object_preview_url

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


get_title.short_description = _('title')


def get_slug(obj):
    return obj.result.slug


get_slug.short_description = _('slug')


def get_site_name(obj):
    return obj.result.site_name


get_site_name.short_description = _('site_name')


def get_language(obj):
    return obj.result.language


get_language.short_description = _('language')


def get_author(obj):
    return obj.result.created_by


get_author.short_description = _('Author')


def get_content_type(obj):
    return obj.result.model.__name__


get_content_type.short_description = _('Content Type')


def get_version_status(obj):
    return obj.result.version_status


get_version_status.short_description = _('Version Status')


def get_modified_date(obj):
    return obj.result.creation_date


get_modified_date.short_description = _('Modified Date')


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
    url = indexes.CharField()

    # admin setting
    list_display = [get_title, get_slug, get_content_type, get_site_name, get_language, get_author,
                    get_version_status, get_modified_date]
    list_filter = [SiteFilter, AuthorFilter, VersionStateFilter, ]
    search_fields = ('text', 'title')
    ordering = ('-id',)
    list_per_page = 50

    model = PageContent

    def prepare_slug(self, obj):
        return obj.page.get_slug(obj.language, fallback=False)

    def prepare_site_id(self, obj):
        return obj.page.node.site_id

    def prepare_site_name(self, obj):
        site_id = obj.page.node.site_id
        return Site.objects.filter(pk=site_id).values_list('domain', flat=True)[0]

    def prepare_plugin_types(self, obj):
        plugin_types = (
            CMSPlugin
            .objects
            .filter(
                placeholder__content_type=ContentType.objects.get_for_model(obj),
                placeholder__object_id=obj.pk,
                language=obj.language,
            )
            .order_by()  # Needed for distinct() with values_list https://code.djangoproject.com/ticket/16058
            .values_list('plugin_type', flat=True)
            .distinct()
        )
        return list(plugin_types)

    def prepare_text(self, obj):
        plugins = CMSPlugin.objects.filter(
            placeholder__content_type=ContentType.objects.get_for_model(obj),
            placeholder__object_id=obj.pk,
            language=obj.language,
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

    def prepare_url(self, obj):
        return get_object_preview_url(obj, obj.language)
