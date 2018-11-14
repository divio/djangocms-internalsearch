from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db.models import Max
from django.db.models.expressions import OuterRef, Subquery
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin, PageContent
from cms.toolbar.utils import get_object_preview_url
from cms.utils.plugins import downcast_plugins

from haystack import indexes
from sekizai.context import SekizaiContext

from djangocms_internalsearch.base import BaseSearchConfig
from djangocms_internalsearch.helpers import (
    get_all_versions,
    get_request,
    get_version_object,
)


from djangocms_versioning.constants import DRAFT, PUBLISHED, UNPUBLISHED
DRAFT, PUBLISHED, UNPUBLISHED = None, None, None


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


def get_version_author(obj):
    return obj.result.version_author


get_version_author.short_description = _('Author')


def get_content_type(obj):
    return obj.result.model.__name__


get_content_type.short_description = _('Content Type')


def get_version_status(obj):
    return obj.result.version_status


get_version_status.short_description = _('Version Status')


def get_modified_date(obj):
    return obj.result.modified_date


get_modified_date.short_description = _('Modified Date')


def get_absolute_url(obj):
    if obj.result.url:
        return format_html("<a href='{url}'>{url}</a>", url=obj.result.url)


def get_published_url(obj):
    if obj.result.published_url:
        return format_html("<a href='{url}'>{url}</a>", url=obj.result.published_url)


def get_url(obj):
    return get_published_url(obj) or get_absolute_url(obj)


get_url.short_description = _('URL')


def annotated_pagecontent_queryset(using=None):
    """Returns a PageContent queryset annotated with latest_pk,
    the primary key corresponding to the latest version
    """
    inner = PageContent._base_manager.filter(
        language=OuterRef('language'),
        page=OuterRef('page')
    ).annotate(
        version=Max('versions__number')
    ).order_by('-version').values('pk')
    return PageContent._base_manager.using(using).annotate(latest_pk=Subquery(inner[:1]))


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
    version_author = indexes.CharField()
    version_status = indexes.CharField()
    modified_date = indexes.DateTimeField()
    is_latest_version = indexes.BooleanField()
    url = indexes.CharField()
    published_url = indexes.CharField()

    # admin setting
    list_display = [get_title, get_slug, get_url, get_content_type, get_site_name,
                    get_language, get_version_author, get_version_status, get_modified_date]
    list_filter = []

    search_fields = ('text', 'title')
    ordering = ('-id',)
    list_per_page = 50

    model = PageContent

    def index_queryset(self, using=None):
        versioning_extension = None
        try:
            versioning_extension = apps.get_app_config('djangocms_versioning').cms_extension
        except (ImportError, LookupError):
            pass

        if versioning_extension and versioning_extension.is_content_model_versioned(self.model):
            return annotated_pagecontent_queryset()
        else:
            return super().index_queryset(using)

    def prepare_slug(self, obj):
        return obj.page.get_slug(obj.language, fallback=False)

    def prepare_modified_date(self, obj):
        changed_date = getattr(obj, 'changed_date')
        creation_date = getattr(obj, 'creation_date')
        version_obj = get_version_object(obj)
        return changed_date if changed_date else creation_date or version_obj.created

    def prepare_site_id(self, obj):
        return obj.page.node.site_id

    def prepare_site_name(self, obj):
        site_id = obj.page.node.site_id
        return Site.objects.filter(pk=site_id).values_list('domain', flat=True)[0]

    def prepare_plugin_types(self, obj):
        plugins = downcast_plugins(
            CMSPlugin
            .objects
            .filter(
                placeholder__content_type=ContentType.objects.get_for_model(obj),
                placeholder__object_id=obj.pk,
                language=obj.language,
            )
        )
        return list(set(plugin.plugin_type for plugin in plugins))

    def prepare_text(self, obj):
        request = get_request(obj.language)
        context = SekizaiContext(request)
        if 'request' not in context:
            context['request'] = request
        renderer = request.toolbar.content_renderer
        return ' '.join(self._render_plugins(obj, context, renderer))

    def prepare_version_status(self, obj):
        version_obj = get_version_object(obj)
        if not version_obj:
            return
        return version_obj.state

    def prepare_version_author(self, obj):
        version_obj = get_version_object(obj)
        if not version_obj:
            return
        return version_obj.created_by.username

    def prepare_url(self, obj):
        return get_object_preview_url(obj, obj.language)

    def prepare_published_url(self, obj):
        if self.prepare_version_status(obj) == PUBLISHED:
            return obj.page.get_absolute_url()
        if self.prepare_version_status(obj) == DRAFT:
            # check if there are published version, to use that URL instead
            version_objs = get_all_versions(obj).filter(state=PUBLISHED)
            if version_objs:
                return obj.page.get_absolute_url()

    def _render_plugins(self, obj, context, renderer):
        for placeholder in obj.get_placeholders():
            yield from renderer.render_plugins(placeholder, obj.language, context)

    def prepare_is_latest_version(self, obj):
        latest_pk = getattr(obj, 'latest_pk', None)
        return obj.pk == latest_pk
