from .helpers import save_to_index


def update_index(sender, operation, request, token, **kwargs):

    from cms.models.titlemodels import Title
    # TODO: generic solution to save index
    save_to_index(Title, operation, request, token, **kwargs)
