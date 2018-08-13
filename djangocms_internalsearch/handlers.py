from django.apps import apps

from .helpers import save_to_index


def update_index(sender, operation, request, token, **kwargs):
    config = apps.get_app_config('djangocms_internalsearch')
    internalsearch_apps_config = config.cms_extension.internalsearch_apps_config
    internalsearch_apps_models = [config.model for config in internalsearch_apps_config]

    # Todo: logic to add for add/update
    if sender in internalsearch_apps_models:
        save_to_index(sender, operation, request, token, **kwargs)
