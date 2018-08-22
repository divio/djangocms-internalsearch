from tempfile import mkdtemp


HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_1',
        'djangocms_internalsearch.test_utils.app_2',
    ],
    'HAYSTACK_CONNECTIONS': {
        'default': {
            'ENGINE': 'djangocms_internalsearch.engine.InternalSearchWhooshTestEngine',
            "PATH": mkdtemp(prefix="test_whoosh_query"),
        },
    }
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_internalsearch', extra_args=[])


if __name__ == '__main__':
    run()
