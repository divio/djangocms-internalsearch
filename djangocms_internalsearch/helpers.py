from .signals import add_to_index


def save_to_index(sender, operation, request, token, **kwargs):
    from cms.models.titlemodels import Title

    if 'obj' in kwargs:
        add_to_index.send(sender=Title, instance=kwargs['obj'])
    elif 'new_plugin' in kwargs:
        add_to_index.send(sender=Title, instance=kwargs['new_plugin'])
