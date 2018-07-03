from mock import Mock
from collections.abc import Iterable

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.apps import apps

from djangocms_internalsearch.cms_config import InternalSearchCMSExtension
from cms import app_registration
from cms.test_utils.testcases import CMSTestCase


class CMSConfigUnitTestCase(CMSTestCase):
    """
    Unit testing for missing cms_config flag
    should raise improperly configured exception
    """

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

        self.assertIsInstance(
            extensions.get_configure_models(cms_config),
            Iterable)


class CMSConfigIntegrationTestCase(CMSTestCase):
    """
    Integration test with another app
    """
    @override_settings(INSTALLED_APPS=[
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_with_search_cms_config',
    ])
    def test_cms_config(self):
        app_registration.autodiscover_cms_configs()
        app = apps.get_app_config('app_with_search_cms_config')
        self.assertTrue(hasattr(app.cms_config, 'internalsearch_models'))

    @override_settings(INSTALLED_APPS=[
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_with_search_missing_config',
    ])
    def test_missing_cms_config(self):
        extensions = InternalSearchCMSExtension()
        app_registration.autodiscover_cms_configs()
        app = apps.get_app_config('app_with_search_missing_config')

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(app.cms_config)
