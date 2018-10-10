from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from djangocms_internalsearch.filters import (
    AuthorFilter,
    ContentTypeFilter,
    LanguageFilter,
    SiteFilter,
    VersionStateFilter,
)


class InternalSearchAdminSetting:
    """
    Default admin setting for all models listing
    """
    list_display = ['title', 'slug', 'get_url', 'content_type', 'site_name', 'language',
                    'author', 'version_status', 'modified_date']
    list_filter = [ContentTypeFilter, AuthorFilter, VersionStateFilter, SiteFilter, LanguageFilter]
    list_per_page = 50
    search_fields = ('text', 'title')
    ordering = ('-id',)

    def has_add_permission(self, request):
        return False

    def modified_date(self, obj):
        return obj.result.creation_date

    def slug(self, obj):
        return obj.result.slug

    def absolute_url(self, obj):
        if obj.result.url:
            return format_html("<a href='{url}'>{url}</a>", url=obj.result.url)
        else:
            return obj.result.url

    absolute_url.short_description = _('URL')
    absolute_url.allow_tags = True

    def published_url(self, obj):
        if obj.result.published_url:
            return format_html("<a href='{url}'>{url}</a>", url=obj.result.published_url)
        else:
            return obj.result.published_url

    published_url.short_description = _('Published URL')
    published_url.allow_tags = True

    def text(self, obj):
        return obj.text

    def title(self, obj):
        return obj.result.title

    def language(self, obj):
        return obj.result.language

    def site_name(self, obj):
        return obj.result.site_name

    def author(self, obj):
        return obj.result.version_author

    def content_type(self, obj):
        return obj.result.model.__name__

    def version_status(self, obj):
        return obj.result.version_status

    def get_url(self, obj):
        return self.published_url(obj) or self.absolute_url(obj)
    get_url.short_description = _('URL')
