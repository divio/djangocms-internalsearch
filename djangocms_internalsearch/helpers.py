from django.apps import apps


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


def get_model_class(model_meta):
    if model_meta:
        app_label, model_name = model_meta.split('.')
        model_class = apps.get_model(app_label, model_name)
        return model_class
    return None
