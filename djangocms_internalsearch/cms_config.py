from collections import Iterable

from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppExtension


class InternalSearchCMSExtension(CMSAppExtension):

    def __init__(self):
        self.internalsearch_apps_config = []

    def configure_app(self, cms_config):
        if hasattr(cms_config, 'internalsearch_app_config'):
            app_config = getattr(cms_config, 'internalsearch_app_config')
            if isinstance(app_config, Iterable):
                self.internalsearch_apps_config.extend(app_config)
            else:
                raise ImproperlyConfigured(
                    "InternalSearch configuration must be a Iterable object")
        else:
            raise ImproperlyConfigured(
                "cms_config.py must have internalsearch_app_config attribute")
