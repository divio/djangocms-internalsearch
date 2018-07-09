from django.apps import apps


def do_index_action(sender, operation, request, token, **kwargs):
    config = apps.get_app_config('djangocms_internalsearch')
    internalsearch_models = config.cms_extension.internalsearch_models

    if sender in internalsearch_models:
        update_index(sender)


def update_index(model):
    # TODO; update object
    pass
