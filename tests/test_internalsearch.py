from mock import Mock, MagicMock

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.apps import apps
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


class CMSConfigIntegrationTestCase(CMSTestCase):
    """
    Integration test with another app
    """
    post_save.connect = MagicMock(name='create_data')
    post_delete.connect = MagicMock(name='delete_data')

    @override_settings(INSTALLED_APPS=[
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_with_search_cms_config',
        'djangocms_internalsearch.test_utils.another_app_with_search_cms_config',
    ])
    def test_cms_config(self):
        setup_cms_apps()
        extensions = InternalSearchCMSExtension()
        app1 = apps.get_app_config('app_with_search_cms_config')
        app2 = apps.get_app_config('another_app_with_search_cms_config')

        self.assertTrue(hasattr(app1.cms_config, 'internalsearch_models'))
        extensions._register_models(app1.label, app1.cms_config.internalsearch_models)

        self.assertTrue(hasattr(app2.cms_config, 'internalsearch_models'))
        extensions._register_models(app2.label, app2.cms_config.internalsearch_models)

        self.assertEqual(len(post_save.connect.mock_calls), 4)
        self.assertEqual(len(post_delete.connect.mock_calls), 4)
    
