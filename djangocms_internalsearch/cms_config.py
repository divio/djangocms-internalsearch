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
    model = Page
    fields = [
        # cms_title
        # prepare
        'page_title',
        # cms_title
        'placehoders_id',
        # cms_title
        # prepare
        'slug',
        # cms_treenode
        'node_id__site_id',
        'language',
        # cms_cmsplugin
        # prepare
        'cmsplugin_type_array',
        # cms_cmsplugin
        # prepare
        'cmsplugin_rendered_source',
        # versioning enable
        # prepare
        'version_status',
        'created_by',
        'changed_by',
        'creation_date',
        'changed_date',
        # prepare from rendered code
        'html_source',
    ]


class CoreCMSAppConfig(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_config_list = [PageModelConfig, ]
