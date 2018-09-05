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
    list_display = ['get_title', 'get_slug', 'get_content_type', 'get_site_name', 'get_language', 'get_author',
                    'get_version_status', 'get_modified_date']
    list_filter = [SiteFilter, AuthorFilter, VersionStateFilter, ]
    search_fields = ('text', 'title')
    ordering = ('-id',)
    list_per_page = 50

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

    def get_modified_date(self, obj):
        return obj.result.creation_date
    get_modified_date.short_description = 'Modified Date'

    def get_slug(self, obj):
        return obj.result.slug
    get_slug.short_description = 'slug'

    def get_title(self, obj):
        return obj.result.title
    get_title.short_description = 'title'

    def get_language(self, obj):
        return obj.result.language
    get_language.short_description = 'language'

    def get_site_name(self, obj):
        return obj.result.site_name
    get_site_name.short_description = 'site_name'

    def get_author(self, obj):
        return obj.result.created_by
    get_author.short_description = 'Author'

    def get_content_type(self, obj):
        return obj.result.model.__name__
    get_content_type.short_description = 'Content Type'

    def get_version_status(self, obj):
        return obj.result.version_status
    get_version_status.short_description = 'Version Status'
