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
from djangocms_internalsearch.test_utils.app_1.cms_config import (
    TestModel3Config,
    TestModel4Config,
)
from djangocms_internalsearch.test_utils.app_1.models import (
    TestModel3,
    TestModel4,
)
from djangocms_internalsearch.test_utils.app_2.cms_config import (
    TestModel1Config,
    TestModel2Config,
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
            internalsearch_config_list=23234,
            app_config=Mock(label='blah_cms_config')
        )

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)

    def test_valid_cms_config_parameter(self):
        extensions = InternalSearchCMSExtension()
        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            internalsearch_config_list=[
                TestModel1Config,
                TestModel2Config,
                TestModel3Config,
                TestModel4Config
            ],
            app_config=Mock(label='blah_cms_config')
        )

        with self.assertNotRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)
            register_model = []
            for app_config in extensions.internalsearch_apps_config:
                register_model.append(app_config.model)

            self.assertTrue(TestModel1 in register_model)
            self.assertTrue(TestModel2 in register_model)
            self.assertTrue(TestModel3 in register_model)
            self.assertTrue(TestModel4 in register_model)


class InternalSearchIntegrationTestCase(CMSTestCase):

    def setUp(self):
        app_registration.get_cms_extension_apps.cache_clear()
        app_registration.get_cms_config_apps.cache_clear()

    def test_config_with_two_apps(self):
        setup_cms_apps()
        internalsearch_config = apps.get_app_config('djangocms_internalsearch')
        apps_config = internalsearch_config.cms_extension.internalsearch_apps_config
        register_model = []

        for app_config in apps_config:
            register_model.append(app_config.model)

        self.assertTrue(TestModel1 in register_model)
        self.assertTrue(TestModel2 in register_model)
        self.assertTrue(TestModel3 in register_model)
        self.assertTrue(TestModel4 in register_model)

    # TODO: Add more intregration test
