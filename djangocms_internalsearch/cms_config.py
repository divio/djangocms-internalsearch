from django.db.models.signals import post_save, post_delete
from django.apps import apps
from django.dispatch import receiver
from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppExtension


class InternalSearchCMSExtension(CMSAppExtension):

    def get_configure_models(self, cms_config):
        """
        Method to fetch configure models from app
        """
        if hasattr(cms_config, 'internalsearch_models'):
            app_models = getattr(cms_config, 'internalsearch_models')
            if isinstance(app_models, (list, tuple)):
                return app_models
            else:
                raise ImproperlyConfigured(
                    "internalsearch_models must be list or tuple objecgit pt"
                )

        else:
            raise ImproperlyConfigured(
                "internalsearch_models must be define in cms_config.py"
            )

    def configure_app(self, cms_config):
        """
        Activated internalsearch models
        """
        app_name = cms_config.app_config.label
        app_models = self.get_configure_models(cms_config)
        if app_name and app_models:
            self._activate_signal(app_name, app_models)

    def _activate_signal(self, app_name, app_models):
        """
        Factory method to generate signal receiver function for each model
        """
        for model in app_models:
            model = apps.get_model(app_name, model)

            @receiver(post_save, sender=model)
            def create_data(model, instance, created, **kwargs):
                # TODO: data massage and create/update object in elastic search
                #       via haystack
                pass

            @receiver(post_delete, sender=model)
            def delete_data(model, instance, created, **kwargs):
                # TODO: delete the object from es
                pass
