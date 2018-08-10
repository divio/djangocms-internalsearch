from haystack import connections

def save_to_index(sender, operation, request, token, **kwargs):

    from cms.models.titlemodels import Title
    from cms.models import CMSPlugin

    index = connections["default"].get_unified_index().get_index(Title)
    if 'obj' in kwargs:
        obj = kwargs['obj'].get_title_obj(request.LANGUAGE_CODE)
    if 'new_plugin' in kwargs:
        #Todo : get title object from placeholder
        obj =kwargs['new_plugin'].placeholder

    index.update_object(obj)
