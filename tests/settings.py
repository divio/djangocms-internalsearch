from tempfile import mkdtemp


HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_1',
        'djangocms_internalsearch.test_utils.app_2',
        'easy_thumbnails',
    ],
    'HAYSTACK_CONNECTIONS': {
        'default': {
            'ENGINE': 'djangocms_internalsearch.engine.InternalSearchWhooshEngine',
            "PATH": mkdtemp(prefix="test_whoosh_query"),
        },
    }
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_internalsearch', extra_args=[])


if __name__ == '__main__':
    run()
