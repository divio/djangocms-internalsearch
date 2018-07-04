from django.db.models.signals import post_save, post_delete
from django.apps import apps
from django.dispatch import receiver
from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppExtension

from .signals import create_data, delete_data


class InternalSearchCMSExtension(CMSAppExtension):

    def get_models_from_config(self, cms_config):
        """
        Method to fetch configure models from app
        """
        if hasattr(cms_config, 'internalsearch_models'):
            app_models = getattr(cms_config, 'internalsearch_models')
            if isinstance(app_models, (list, tuple)):
                return app_models
            else:
                raise ImproperlyConfigured(
                    "internalsearch_models must be a list or tuple object")

        else:
            raise ImproperlyConfigured(
                "internalsearch_models must be defined in cms_config.py")

    def configure_app(self, cms_config):
        """
        Register model classes defined in config for internal search
        """
        app_name = cms_config.app_config.label
        app_models = self.get_models_from_config(cms_config)
        self._register_models(app_name, app_models)

    def _register_models(self, app_name, app_models):
        """
        Register models with haystack
        """
        for model in app_models:
            model = apps.get_model(app_name, model)
            post_save.connect(create_data, sender=model)
            post_delete.connect(delete_data, sender=model)
