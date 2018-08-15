from haystack import connections


def save_to_index(sender, operation, request, token, **kwargs):

    from cms.models.titlemodels import Title
    from cms.utils import get_language_from_request

    index = connections["default"].get_unified_index().get_index(Title)
    if 'obj' in kwargs:
        obj = kwargs['obj'].get_title_obj(get_language_from_request(request, current_page=kwargs['obj']))
        if operation == 'delete_page':
            index.remove_object(obj)
        else:
            index.update_object(obj)
    if 'new_plugin' in kwargs:
        plc = kwargs['new_plugin'].placeholder
        obj = plc.page.get_title_obj(get_language_from_request(request, current_page=plc.page))
        index.update_object(obj)
    if 'placeholder' in kwargs:
        plc = kwargs['placeholder']
        obj = plc.page.get_title_obj(get_language_from_request(request, current_page=plc.page))
        if operation is 'delete_plugin':
            index.remove_object(obj)
        else:
            index.update_object(obj)

