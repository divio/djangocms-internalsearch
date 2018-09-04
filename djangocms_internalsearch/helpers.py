from cms.operations import DELETE_PAGE, DELETE_PLUGIN

from haystack import connections


def save_to_index(sender, operation, request, token, **kwargs):
    from django.utils.translation import get_language_from_request

    from cms.models.titlemodels import Title

    if 'obj' in kwargs:
        index = connections["default"].get_unified_index().get_index(Title)
        obj = kwargs['obj'].get_title_obj(get_language_from_request(request))
        save_object(index, obj, operation)

    if 'new_plugin' in kwargs:
        index = connections["default"].get_unified_index().get_index(Title)
        plc = kwargs['new_plugin'].placeholder
        obj = plc.page.get_title_obj(get_language_from_request(request))
        index.update_object(obj)

    if 'plugin' in kwargs:
        try:
            plugin = kwargs['plugin']
            index = connections["default"].get_unified_index().get_index(type(plugin))
            save_object(index, obj, operation)
        except:
            pass


def save_object(index, obj, operation):
    if operation in [DELETE_PLUGIN, DELETE_PAGE]:
        index.remove_object(obj)
    else:
        index.update_object(obj)
