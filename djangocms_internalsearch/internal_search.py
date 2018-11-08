from django.utils.html import format_html

from djangocms_internalsearch.filters import (
    AuthorFilter,
    ContentTypeFilter,
    LanguageFilter,
    LatestVersionFilter,
    SiteFilter,
    VersionStateFilter,
)


class InternalSearchAdminSetting:
    """
    Default admin setting for all models listing
    """

    class Media:
        js = ('djangocms_internalsearch/js/actions.js',)
        css = {
            'all': ('djangocms_internalsearch/css/custom.css',)
        }

    list_display = ['title', 'slug', 'url', 'content_type', 'version_status', 'locked', 'modified_date',
                    'author', 'site_name', 'language', ]
    list_filter = [ContentTypeFilter, AuthorFilter, VersionStateFilter, LatestVersionFilter, SiteFilter, LanguageFilter]
    list_per_page = 50
    search_fields = ('text', 'title')
    ordering = ('-id',)

    def has_add_permission(self, request):
        return False

    def modified_date(self, obj):
        return obj.result.modified_date

    def slug(self, obj):
        return obj.result.slug

    def absolute_url(self, obj):
        if obj.result.url:
            return format_html(
                '<a class="js-internal-search-close-sideframe" target="_top" href="{url}">{url}</a>',
                url=obj.result.url,
            )
        else:
            return obj.result.url

    absolute_url.allow_tags = True

    def published_url(self, obj):
        if obj.result.published_url:
            return format_html(
                '<a class="js-internal-search-close-sideframe" target="_top" href="{url}">{url}</a>',
                url=obj.result.published_url,
            )
        else:
            return obj.result.published_url

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

    def locked(self, obj):
        if obj.result.locked == 'True':
            return format_html(
                "<img class='cms-version-locked-status-icon' "
                "src='/static/djangocms_version_locking/svg/lock.svg' title='locked' />")

    def url(self, obj):
        return self.published_url(obj) or self.absolute_url(obj)
