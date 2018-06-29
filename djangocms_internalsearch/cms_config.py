from django.db.models.signals import post_save, post_delete
from django.apps import apps
from django.dispatch import receiver
from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppExtension


class InternalSearchCMSExtension(CMSAppExtension):

    def configure_app(self, cms_config):
        """
        get activated internalsearch models
        """
        app_name = cms_config.app_config.label

        if hasattr(cms_config, 'internalsearch_models'):
            app_models = getattr(cms_config, 'internalsearch_models')
            self._activate_signal(app_name, app_models)
        else:
            raise ImproperlyConfigured(
                "internalsearch_models must be define in cms_config.py"
            )

    def _activate_signal(self, app_name, app_models):
        """
        factory method to generate signal receiver function for each model
        """
        for model in app_models:
            model = apps.get_model(app_name, model)

            @receiver(post_save, sender=model)
            def create_data(model, instance, created, **kwargs):
                # TODO: data massage and create/update object in elastic search via haystack
                pass

            @receiver(post_delete, sender=model)
            def delete_data(model, instance, created, **kwargs):
                # TODO: delete the object from es
                pass
