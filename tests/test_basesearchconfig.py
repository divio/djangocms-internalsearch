from unittest.mock import Mock

from django.apps import apps

from cms import app_registration
from cms.utils.setup import setup_cms_apps

from .utils import TestCase


class InternalSearchConfigTestCase(TestCase):

    def setUp(self):
        app_registration.get_cms_extension_apps.cache_clear()
        app_registration.get_cms_config_apps.cache_clear()

    def test_search_config_with_expected_method(self):
        setup_cms_apps()
        internalsearch_config = apps.get_app_config('djangocms_internalsearch')
        registered_configs = internalsearch_config.cms_extension.internalsearch_apps_config
        expected_method = ['prepare_text', 'prepare_content_type']
        obj = Mock()
        with self.assertNotRaises(NotImplementedError):
            for config in registered_configs:
                for attr in expected_method:
                    getattr(config, attr)(self, obj)

    def test_search_config_with_expected_attributes(self):
        setup_cms_apps()
        internalsearch_config = apps.get_app_config('djangocms_internalsearch')
        registered_configs = internalsearch_config.cms_extension.internalsearch_apps_config
        expected_attributes = ['model', 'list_display']
        with self.assertNotRaises(NotImplementedError):
            for config in registered_configs:
                for attr in expected_attributes:
                    self.assertTrue(attr in config.__dict__)
