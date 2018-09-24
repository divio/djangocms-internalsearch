from collections import Iterable

from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppConfig, CMSAppExtension

from djangocms_internalsearch.contrib.cms.internal_search import (
    PageContentConfig,
)


try:
    from djangocms_internalsearch.contrib.filer.internal_search import (
        FilerFileConfig,
        FilerImageConfig,
    )
except ImportError:
    FilerFileConfig = FilerImageConfig = None

try:
    from djangocms_internalsearch.contrib.alias.internal_search import AliasContentConfig
except ImportError:
    AliasContentConfig = None


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
    if FilerFileConfig:
        internalsearch_config_list += [
            FilerFileConfig,
            FilerImageConfig,
        ]
    if AliasContentConfig:
        internalsearch_config_list += [
            AliasContentConfig
        ]
