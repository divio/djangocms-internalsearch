import os
from tempfile import mkdtemp


ENVIRONMENT_APPS = [('ENABLE_VERSIONING', 'djangocms_versioning'),
                    ('ENABLE_FILER', 'filer')]


def get_enabled_apps(extra_apps):
    enabled_apps = []
    for enable_flag, app in extra_apps:
        if bool(os.environ.get(enable_flag, False)):
            enabled_apps.append(app)

    return enabled_apps


HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_1',
        'djangocms_internalsearch.test_utils.app_2',
        'easy_thumbnails',
    ] + get_enabled_apps(ENVIRONMENT_APPS),
    'HAYSTACK_CONNECTIONS': {
        'default': {
            'ENGINE': 'djangocms_internalsearch.backends.whoosh.InternalSearchWhooshEngine',
            "PATH": mkdtemp(prefix="test_whoosh_query"),
        },
    },
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_internalsearch', extra_args=[])


if __name__ == '__main__':
    run()
