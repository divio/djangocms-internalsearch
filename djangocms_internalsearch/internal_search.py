from cms.models import Page

from haystack import indexes

from .base import BaseSearchConfig


class PageContentConfig(BaseSearchConfig):
    """
    Page config and also index defination
    """
    title = indexes.CharField()
    slug = indexes.CharField()
    site_id = indexes.IntegerField()
    site_name = indexes.CharField()
    language = indexes.CharField()
    plugin_types = indexes.MultiValueField()
    created_by = indexes.CharField(model_attr='created_by')
    changed_by = indexes.CharField(model_attr='changed_by')
    version_status = indexes.CharField()
    creation_date = indexes.DateTimeField(model_attr='creation_date')
    changed_date = indexes.DateTimeField(model_attr='changed_date')

    # model class attribute
    model = Page

    # admin setting
    list_display = ('page_title', 'language', 'version_status', 'changed_by')
    list_filter = ('language', 'site_name', 'changed_by',)

    def prepare_title(self, obj):
        # TODO: prepare title (cms_title) field to save
        pass

    def prepare_slug(self, obj):
        # TODO: prepare slug/url (cms_title) to save
        pass

    def prepare_site_name(self, obj):
        # TODO: prepare sitename (cms_treenode) to save
        pass

    def prepare_plugin_types(self, obj):
        # TODO: preapare list of cms plugin (cms_plugin) used for specific page
        pass

    def prepare_content_type(self, obj):
        # TODO: perpare text as string to get rendered data of all cms plugin for
        # specific page
        pass

    def prepare_text(self, obj):
        # TODO: perpare text as string to get rendered data of all cms plugin for
        # specific page
        pass
