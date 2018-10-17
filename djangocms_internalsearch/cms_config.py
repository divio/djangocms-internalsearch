from collections import Iterable
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppConfig, CMSAppExtension

from djangocms_internalsearch.contrib.cms.internal_search import (
    PageContentConfig,
)

try:
    apps.get_app_config('filer')
    from djangocms_internalsearch.contrib.filer.internal_search import filer_model_config_factory
except (LookupError, ImportError):
    filer_model_config_factory = None


class InternalSearchCMSExtension(CMSAppExtension):

    def __init__(self):
        self.internalsearch_apps_config = []

    def configure_app(self, cms_config):
        if hasattr(cms_config, 'internalsearch_config_list'):
            internalsearch_config_list = getattr(cms_config, 'internalsearch_config_list')
            if isinstance(internalsearch_config_list, Iterable):
                self.internalsearch_apps_config.extend(internalsearch_config_list)
            else:
                raise ImproperlyConfigured(
                    "InternalSearch configuration must be a Iterable object")
        else:
            raise ImproperlyConfigured(
                "cms_config.py must have internalsearch_config_list attribute")


class CoreCMSAppConfig(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_config_list = [
        PageContentConfig,
    ]
    if filer_model_config_factory:
        internalsearch_config_list.extend(
            filer_model_config_factory()
        )
