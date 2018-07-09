from django.apps import apps

from cms import operations


def do_search_action(sender, operation, request, token, **kwargs):
    config = apps.get_app_config('djangocms_internalsearch')
    internalsearch_models = config.cms_extension.internalsearch_models

    if sender in internalsearch_models:
        if operation in [operations.DELETE_PAGE, operations.DELETE_PLUGIN]:
            remove_from_index()
        else:
            update_to_index()


def update_to_index():
    # TODO; add or update object
    pass


def remove_from_index():
    # TODO: delete the object
    pass
