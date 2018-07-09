from django.apps import apps

from cms import operations


def do_index_action(sender, operation, request, token, **kwargs):
    config = apps.get_app_config('djangocms_internalsearch')
    internalsearch_models = config.cms_extension.internalsearch_models

    if sender in internalsearch_models:
        if operation in [
            operations.DELETE_PAGE,
            operations.DELETE_PLUGIN
        ]:
            remove_from_index(sender)
        elif operation in [
            operations.ADD_PLUGIN,
            operations.ADD_PAGE_TRANSLATION
        ]:
            add_to_index(sender)
        else:
            update_index(sender)


def add_to_index(model):
    # TODO; add object
    pass


def update_index(model):
    # TODO; update object
    pass


def remove_from_index(model):
    # TODO: delete the object
    pass
