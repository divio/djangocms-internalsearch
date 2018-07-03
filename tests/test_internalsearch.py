from mock import patch, Mock
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.db.models.signals import post_save, post_delete

from djangocms_internalsearch.cms_config import InternalSearchCMSExtension
from cms import app_registration
from cms.test_utils.testcases import CMSTestCase
from cms.utils.setup import setup_cms_apps


class CMSConfigUnitTestCase(CMSTestCase):

    def test_missing_cms_config_flag(self):
        """
        Missing cms config flag case
        """
        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            app_config=Mock(label='blah_cms_config'))

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)

    def test_cms_config_flag(self):
        """
        Valid cms config flag case
        """
        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            internalsearch_models=['TestModel', ],
            app_config=Mock(label='another_blah_cms_config'))

        self.assertListEqual(
            extensions.get_models_from_config(cms_config),
            ['TestModel'])

    def test_invalid__cms_config_parameter(self):
        """
        improperly cms config flag case
        """
        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            internalsearch_models='TestModel',
            app_config=Mock(label='blah_cms_config'))

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)


class CMSConfigIntegrationTestCase(CMSTestCase):
    """
    Integration test with two apps
    """
    def setUp(self):
        app_registration.get_cms_extension_apps.cache_clear()
        app_registration.get_cms_config_apps.cache_clear()

    @override_settings(INSTALLED_APPS=[
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_with_search_cms_config',
        'djangocms_internalsearch.test_utils.another_app_with_search_cms_config',
    ])
    @patch.object(post_save, 'connect')
    @patch.object(post_delete, 'connect')
    def test_integration_with_other_apps(self, mock_post_delete, mock_post_save):
        setup_cms_apps()
        self.assertEqual(mock_post_delete.call_count, 4)
        self.assertEqual(mock_post_save.call_count, 4)
