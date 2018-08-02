from cms.models.titlemodels import Title

from haystack import indexes

from .base import BaseSearchConfig


class PageContentConfig(BaseSearchConfig):
    """
    Page config and index definition
    """
    page = indexes.IntegerField(model_attr='page')
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

    # admin setting
    list_display = ('page_title', 'language', 'version_status', 'changed_by')
    list_filter = ('language', 'site_name', 'changed_by',)

    def prepare_site_id(self, obj):
        # TODO: prepare site_ud (cms_treenode) to save
        pass

    def prepare_site_name(self, obj):
        # TODO: prepare sitename (cms_treenode) to save
        pass

    def prepare_plugin_types(self, obj):
        # TODO: preapare list of cms plugin (cms_plugin) used for specific page
        pass

    def prepare_text(self, obj):
        # TODO: perpare text as string to get rendered data of all cms plugin for
        # specific page
        pass

    def prepare_created_by(self, obj):
        # TODO: prepare from page model
        pass
