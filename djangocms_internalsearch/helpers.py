from haystack import connections


def save_to_index(sender, operation, request, token, **kwargs):

    from django.utils.translation import get_language_from_request
    from cms.operations import DELETE_PAGE, DELETE_PLUGIN
    from cms.models.titlemodels import Title
    from filer.models.filemodels import File
    from filer.models.imagemodels import Image

    if 'obj' in kwargs:
        index = connections["default"].get_unified_index().get_index(Title)
        obj = kwargs['obj'].get_title_obj(get_language_from_request(request, check_path=False))
        if operation == DELETE_PAGE:
            index.remove_object(obj)
        else:
            index.update_object(obj)
    if 'new_plugin' in kwargs:
        index = connections["default"].get_unified_index().get_index(Title)
        plc = kwargs['new_plugin'].placeholder
        obj = plc.page.get_title_obj(get_language_from_request(request, check_path=False))
        index.update_object(obj)
    if 'plugin' in kwargs:
        plugin_type = kwargs['plugin'].plugin_type
        if plugin_type is 'TextPlugin':
            index = connections["default"].get_unified_index().get_index(Title)
        if plugin_type is 'FilePlugin':
            index = connections["default"].get_unified_index().get_index(File)
        if plugin_type is 'ImagePlugin':
            index = connections["default"].get_unified_index().get_index(Image)

        obj = kwargs['placeholder'].page.get_title_obj(get_language_from_request(request, check_path=False))
        if operation is DELETE_PLUGIN:
            index.remove_object(obj)
        else:
            index.update_object(obj)
