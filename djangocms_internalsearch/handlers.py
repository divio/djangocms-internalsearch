from django.apps import apps

from .helpers import save_to_index


def update_index(sender, operation, request, token, **kwargs):
    config = apps.get_app_config('djangocms_internalsearch')
    internalsearch_models = config.cms_extension.internalsearch_apps_config

    from cms.models.titlemodels import Title
    from cms.models import Page
    from cms.admin.pageadmin import PageAdmin

    if sender in [Title, Page, PageAdmin]:
        save_to_index(Title, operation, request, token, **kwargs)

