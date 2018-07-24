from collections import Iterable

from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppExtension


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
