try:
    from unittest.mock import Mock
except ImportError:
    raise "InternalSearch app requires Python 3.3 or above"


from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

from cms import app_registration
from cms.test_utils.testcases import CMSTestCase
from cms.utils.setup import setup_cms_apps

from djangocms_internalsearch.cms_config import InternalSearchCMSExtension
from djangocms_internalsearch.test_utils.app_1.models import (
    TestModel3,
    TestModel4,
)
from djangocms_internalsearch.test_utils.app_2.models import (
    TestModel1,
    TestModel2,
)

from .utils import TestCase


class InternalSearchUnitTestCase(CMSTestCase, TestCase):

    def test_missing_cms_config(self):
        extensions = InternalSearchCMSExtension()
        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            app_config=Mock(label='blah_cms_config')
        )

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)

    def test_invalid_cms_config_parameter(self):
        extensions = InternalSearchCMSExtension()
        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            search_models=23234,
            app_config=Mock(label='blah_cms_config')
        )

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)

    def test_valid_cms_config_parameter(self):
        extensions = InternalSearchCMSExtension()
        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            search_models=[TestModel1, TestModel2, TestModel3, TestModel4],
            app_config=Mock(label='blah_cms_config')
        )

        with self.assertNotRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)
            self.assertTrue(TestModel1 in extensions.internalsearch_models)
            self.assertTrue(TestModel2 in extensions.internalsearch_models)
            self.assertTrue(TestModel3 in extensions.internalsearch_models)
            self.assertTrue(TestModel4 in extensions.internalsearch_models)


class InternalSearchIntegrationTestCase(CMSTestCase):

    def setUp(self):
        app_registration.get_cms_extension_apps.cache_clear()
        app_registration.get_cms_config_apps.cache_clear()

    def test_config_with_two_apps(self):
        setup_cms_apps()
        internalsearch_config = apps.get_app_config('djangocms_internalsearch')
        registered_model = internalsearch_config.cms_extension.internalsearch_models
        self.assertEqual(len(registered_model), 4)

    # TODO: Add more intregration test
