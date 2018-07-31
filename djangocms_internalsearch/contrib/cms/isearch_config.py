from cms.models import Page

from djangocms_internalsearch.base import BaseConfig

from .indexes import PageContentIndex


class PageConfig(BaseConfig):
    model = Page
    fields = [
        'page_title', 'slug', 'site_id', 'site_name', 'language',
        'cmsplugin_type_array', 'text', 'created_by', 'changed_by',
        'version_status', 'creation_date', 'changed_date', 'html_source',
    ]
    list_display = ('page_title', 'language', 'version_status', 'changed_by')
    list_filter = ('language', 'site_name', 'changed_by',)
    index = PageContentIndex
