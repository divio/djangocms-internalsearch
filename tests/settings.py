HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'djangocms_internalsearch',
        # 'djangocms_internalsearch.test_utils.project.app_with_cms_config'

    ],
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_internalsearch',  extra_args=[])


if __name__ == '__main__':
    run()
