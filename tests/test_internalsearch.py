from mock import Mock

from django.core.exceptions import ImproperlyConfigured

from djangocms_internalsearch.cms_config import InternalSearchCMSExtension
from cms import app_registration
from cms.test_utils.testcases import CMSTestCase
from django.test import override_settings
from django.apps import apps, AppConfig


class CMSConfigUnitTestCase(CMSTestCase):
    """unit testing for missing cms_config flag
    should raise improperly configured exception """

    def test_missing_cms_config_flag(self):
        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            app_config=Mock(label='blah_cms_config')
            )

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)


class CMSConfigIntegrationTestCase(CMSTestCase):
    """
    Intregartion test with another app
    """
    @override_settings(INSTALLED_APPS=[
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_with_search_cms_config',
    ])
    def test_cms_config(self):
        app_registration.autodiscover_cms_configs()
        app = apps.get_app_config('app_with_search_cms_config')
        self.assertTrue(hasattr(app.cms_config, 'internalsearch_models'))
