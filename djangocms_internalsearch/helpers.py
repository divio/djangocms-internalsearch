from django.apps import apps
from django.conf import settings
from django.test import RequestFactory


def save_to_index(sender, operation, request, token, **kwargs):
    # TODO; add/update object
    pass


def get_internalsearch_model_config(model_class):
    internalsearch_config = apps.get_app_config('djangocms_internalsearch')
    apps_config = internalsearch_config.cms_extension.internalsearch_apps_config
    app_config = [app for app in apps_config if app.model == model_class]
    return app_config[0]


def get_internalsearch_config():
    internalsearch_config = apps.get_app_config('djangocms_internalsearch')
    apps_config = internalsearch_config.cms_extension.internalsearch_apps_config
    return apps_config


def get_request(language=None):
    from django.contrib.auth.models import AnonymousUser
    from cms.toolbar.toolbar import CMSToolbar
    """
    Returns a Request instance populated with cms specific attributes.
    """
    request_factory = RequestFactory(HTTP_HOST=settings.ALLOWED_HOSTS[0])
    request = request_factory.get("/")
    request.session = {}
    request.LANGUAGE_CODE = language or settings.LANGUAGE_CODE
    # Needed for plugin rendering.
    request.current_page = None
    request.user = AnonymousUser()
    request.toolbar = CMSToolbar(request)
    return request
