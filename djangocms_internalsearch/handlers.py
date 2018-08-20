from .helpers import save_to_index


def update_index(sender, operation, request, token, **kwargs):

    from cms.models.titlemodels import Title
    from cms.models import Page
    from cms.admin.pageadmin import PageAdmin

    if sender in [Title, Page, PageAdmin]:
        save_to_index(Title, operation, request, token, **kwargs)

