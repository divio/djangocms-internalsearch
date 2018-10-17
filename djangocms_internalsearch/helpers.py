from django.apps import apps
from django.conf import settings
from django.test import RequestFactory
from django.utils.translation import get_language_from_request

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

from .signals import content_object_delete, content_object_state_change


def delete_page(index, request, **kwargs):
    from cms.models import Page, PageContent

    obj = kwargs['obj']

    # obj is PageContent then remove from index
    if isinstance(obj, PageContent):
        index.remove_object(obj)
        return

    cms_pages = [obj, ]
    if obj.node.is_branch:
        nodes = obj.node.get_descendants()
        cms_pages.extend(Page.objects.filter(node__in=nodes))

    page_content_objs = PageContent._base_manager.filter(page__in=cms_pages)

    for page_content in page_content_objs:
        index.remove_object(page_content)


def update_page_content(index, request, **kwargs):
    obj = kwargs['obj'].get_title_obj(get_language_from_request(request))
    index.update_object(obj)


def delete_page_content(index, request, **kwargs):
    obj = kwargs['obj'].get_title_obj(get_language_from_request(request))
    index.remove_object(obj)


def update_plugin(index, request, **kwargs):
    index.update_object(kwargs['placeholder'].source)


def delete_plugin(index, request, **kwargs):
    index.update_object(kwargs['placeholder'].source)


def move_plugin(index, request, **kwargs):
    index.update_object(kwargs['source_placeholder'].source)
    index.update_object(kwargs['target_placeholder'].source)


def save_to_index(sender, operation, request, token, **kwargs):
    plugin_actions = [ADD_PLUGIN, CHANGE_PLUGIN, DELETE_PLUGIN, MOVE_PLUGIN]
    if operation in plugin_actions:
        placeholder_field = (
            'target_placeholder' if operation == MOVE_PLUGIN else 'placeholder'
        )
        source = kwargs[placeholder_field].source
        if source is None:
            # plugin operation on a placeholder without source,
            # there's nothing to update
            return
        content_model = source.__class__
        register_models = [config.model for config in get_internalsearch_config()]
        if content_model not in register_models:
            return
    else:
        from cms.models import PageContent
        content_model = PageContent

    index = get_model_index(content_model)

    operation_actions = {
        ADD_PAGE_TRANSLATION: update_page_content,
        CHANGE_PAGE_TRANSLATION: update_page_content,
        ADD_PLUGIN: update_plugin,
        CHANGE_PLUGIN: update_plugin,
        DELETE_PLUGIN: delete_plugin,
        MOVE_PLUGIN: move_plugin,
    }

    if operation not in operation_actions:
        return

    operation_actions[operation](index, request, **kwargs)


def remove_from_index(sender, operation, request, token, **kwargs):

    from cms.models import PageContent
    index = get_model_index(PageContent)

    if operation not in [DELETE_PAGE, DELETE_PAGE_TRANSLATION]:
        return

    delete_page(index, request, **kwargs)


def content_object_state_change_receiver(sender, content_object, **kwargs):
    """
    Signal receiver for content object state change.
    Responds to all Versionable content object
    """
    content_model = content_object.__class__
    # check if content object type is in app config registry
    try:
        get_internalsearch_model_config(content_model)
    except IndexError:
        return
    index = get_model_index(content_model)
    index.update_object(content_object)


def content_object_delete_receiver(sender, content_object, **kwargs):
    """
    Signal receiver for content object delete.
    Responds to all Versionable content object
    """
    content_model = content_object.__class__
    # check if content object type is in app config registry
    try:
        get_internalsearch_model_config(content_model)
    except IndexError:
        return
    index = get_model_index(content_model)
    index.remove_object(content_object)


def emit_content_change(obj, sender=None):
    """
    Sends a content object state change signal if obj class is registered by
    internalsearch.
    Helper function to be used in apps that integrates with internalsearch.
    """
    try:
        get_internalsearch_model_config(obj.__class__)
    except (IndexError, LookupError):
        # Internal search is not install or model is not registered with internal search
        return

    content_object_state_change.send(
        sender=sender or obj.__class__,
        content_object=obj,
    )


def emit_content_delete(obj, sender=None):
    """
    Sends a content object delete signal if obj class is registered by
    internalsearch.
    Helper function to be used in apps that integrates with internalsearch.
    """
    try:
        get_internalsearch_model_config(obj.__class__)
    except (IndexError, LookupError):
        # Internal search is not install or model is not registered with internal search
        return

    content_object_delete.send(
        sender=sender or obj.__class__,
        content_object=obj,
    )


def get_internalsearch_model_config(model_class):
    internalsearch_config = apps.get_app_config('djangocms_internalsearch')
    apps_config = internalsearch_config.cms_extension.internalsearch_apps_config
    app_config = [app for app in apps_config if app.model == model_class]
    return app_config[0]


def get_internalsearch_config():
    internalsearch_config = apps.get_app_config('djangocms_internalsearch')
    apps_config = internalsearch_config.cms_extension.internalsearch_apps_config
    return apps_config


def get_moderated_models():
    try:
        moderation_config = apps.get_app_config('djangocms_moderation')
        return moderation_config.cms_extension.moderated_models
    except LookupError:
        return []


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


def get_version_object(obj):
    try:
        from djangocms_versioning.models import Version
    except ImportError:
        return
    return Version.objects.get_for_content(obj)


def get_model_index(content_model):
    from haystack import connections
    # FIXME Don't hardcode 'default' connection
    return connections["default"].get_unified_index().get_index(content_model)
