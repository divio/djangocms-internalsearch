from collections import Iterable

from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppExtension
from .search_util import create_search_index_for_haystack


class InternalSearchCMSExtension(CMSAppExtension):

    def __init__(self):
        self.internalsearch_models = []

    def configure_app(self, cms_config):

        if hasattr(cms_config, 'search_models'):
            app_models = getattr(cms_config, 'search_models')
            if isinstance(app_models, Iterable):
                self.internalsearch_models.extend(app_models)
                create_search_index_for_haystack(app_models)
            else:
                raise ImproperlyConfigured(
                    "models configuration for internalsearch must be a Iterable object")

        else:
            raise ImproperlyConfigured(
                "internalsearch expect models configuration defined in cms_config.py")

