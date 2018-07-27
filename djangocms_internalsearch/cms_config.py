from collections import Iterable

from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppConfig, CMSAppExtension
from cms.models.pagemodel import Page


class InternalSearchCMSExtension(CMSAppExtension):

    def __init__(self):
        self.internalsearch_models = []

    def configure_app(self, cms_config):
        if hasattr(cms_config, 'internalsearch_config_list'):
            app_config_list = getattr(cms_config, 'internalsearch_config_list')
            if isinstance(app_config_list, Iterable):
                self.internalsearch_models.extend(
                    app_config.model for app_config in app_config_list
                )
            else:
                raise ImproperlyConfigured(
                    "InternalSearch configuration must be a Iterable object")
        else:
            raise ImproperlyConfigured(
                "cms_config.py must have internalsearch_config_list attribute")


class PageModelConfig:
    """
    Prepare fields from:
    page_title > cms_title
    slug > cms_title
    site_id > cms_treenode__site_id
    cmsplugin_type_array > cms_cmsplugin
    text > cms_plugin rendered source in single string
    html_source > html source of whole page
    """
    model = Page
    fields = [
        'page_title', 'slug', 'site_id', 'site_name', 'language',
        'cmsplugin_type_array', 'text', 'created_by', 'changed_by',
        'version_status', 'creation_date', 'changed_date', 'html_source',
    ]

    list_display = ('page_title', 'language', 'version_status', 'changed_by')
    list_filter = ('language', 'site_name', 'changed_by',)
    auto_create_index_fields = False


class CoreCMSAppConfig(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_config_list = [PageModelConfig, ]
