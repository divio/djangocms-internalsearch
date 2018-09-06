from cms.operations import (
    ADD_PAGE_TRANSLATION,
    ADD_PLUGIN,
    CHANGE_PAGE_TRANSLATION,
    CHANGE_PLUGIN,
    DELETE_PAGE,
    DELETE_PAGE_TRANSLATION,
    DELETE_PLUGIN,
    MOVE_PLUGIN,
)

from django.utils.translation import get_language_from_request

from haystack import connections


def delete_page(index, request, **kwargs):
    obj = kwargs['obj'].get_title_obj(get_language_from_request(request))
    index.remove_object(obj)


def update_page_content(index, request, **kwargs):
    obj = kwargs['obj'].get_title_obj(get_language_from_request(request))
    index.update_object(obj)


def delete_page_content(index, request, **kwargs):
    obj = kwargs['obj'].get_title_obj(get_language_from_request(request))
    index.remove_object(obj)


def update_plugin(index, request, **kwargs):
    index.update_object(kwargs['placeholder'].source)


def delete_plugin(index, request, **kwargs):
    index.remove_object(kwargs['placeholder'].source)


def move_plugin(index, request, **kwargs):
    index.update_object(kwargs['source_placeholder'].source)
    index.update_object(kwargs['target_placeholder'].source)


def save_to_index(sender, operation, request, token, **kwargs):
    from cms.models import PageContent

    index = connections["default"].get_unified_index().get_index(PageContent)

    operation_actions = {
        DELETE_PAGE: delete_page,
        ADD_PAGE_TRANSLATION: update_page_content,
        CHANGE_PAGE_TRANSLATION: update_page_content,
        DELETE_PAGE_TRANSLATION: delete_page_content,
        ADD_PLUGIN: update_plugin,
        CHANGE_PLUGIN: update_plugin,
        DELETE_PLUGIN: delete_plugin,
        MOVE_PLUGIN: move_plugin,
    }

    if operation not in operation_actions:
        return

    operation_actions[operation](index, request, **kwargs)
