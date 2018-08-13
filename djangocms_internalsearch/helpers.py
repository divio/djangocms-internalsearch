from haystack import connections


def save_to_index(sender, operation, request, token, **kwargs):

    from cms.models.titlemodels import Title

    index = connections["default"].get_unified_index().get_index(Title)
    if 'obj' in kwargs:
        obj = kwargs['obj'].get_title_obj(request.LANGUAGE_CODE)
        if operation is 'delete_page':
            index.remove_object(obj)
        else:
            index.update_object(obj)
    if 'new_plugin' in kwargs:
        plc =kwargs['new_plugin'].placeholder
        obj = plc.page_getter().get_title_obj(request.LANGUAGE_CODE)
        index.update_object(obj)
    if 'placeholder' in kwargs:
        plc = kwargs['placeholder']
        obj = plc.page_getter().get_title_obj(request.LANGUAGE_CODE)
        if operation is 'delete_plugin':
            index.remove_object(obj)
        else:
            index.update_object(obj)

