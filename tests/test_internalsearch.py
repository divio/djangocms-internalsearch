try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import patch, Mock

from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_delete, post_save

from cms import app_registration
from cms.test_utils.testcases import CMSTestCase
from cms.utils.setup import setup_cms_apps

from djangocms_internalsearch.cms_config import InternalSearchCMSExtension
from djangocms_internalsearch.signals import create_data, delete_data
from djangocms_internalsearch.test_utils.another_app_with_search_cms_config.models import (
TestModel1,
TestModel2,
)
from djangocms_internalsearch.test_utils.app_with_search_cms_config.models import (
    TestModel3,
    TestModel4,
)


class CMSConfigUnitTestCase(CMSTestCase):

    def test_missing_cms_config(self):

        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            app_config=Mock(label='blah_cms_config'))

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)

    def test_valid_cms_config(self):

        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            internalsearch_models=['TestModel', ],
            app_config=Mock(label='another_blah_cms_config'))

        self.assertListEqual(
            extensions.get_models_from_config(cms_config),
            ['TestModel'])

    def test_invalid_cms_config_parameter(self):

        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            internalsearch_models='TestModel',
            app_config=Mock(label='blah_cms_config'))

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)


class CMSConfigIntegrationTestCase(CMSTestCase):

    def setUp(self):
        app_registration.get_cms_extension_apps.cache_clear()
        app_registration.get_cms_config_apps.cache_clear()

    @patch.object(post_save, 'connect')
    @patch.object(post_delete, 'connect')
    def test_integration_with_other_apps(self, mock_post_delete, mock_post_save):
        setup_cms_apps()

        # check of howmany mock methods has been call
        # Test utils has two apps with two models so expecting
        # method to call four times.
        self.assertEqual(mock_post_delete.call_count, 4)
        self.assertEqual(mock_post_save.call_count, 4)

        # call_args_list contains all call records so test here to check
        # create_data have been called with expected four models. Order of
        # model(TestModel3, TestModel4 etc...) varies depand on
        # order of app appears on INSTALLED_APPS
        self.assertEqual(mock_post_save.call_args_list[0][0][0],  create_data)
        self.assertEqual(mock_post_save.call_args_list[0][1]['sender'], TestModel3)
        self.assertEqual(mock_post_save.call_args_list[1][0][0],  create_data)
        self.assertEqual(mock_post_save.call_args_list[1][1]['sender'], TestModel4)
        self.assertEqual(mock_post_save.call_args_list[2][0][0],  create_data)
        self.assertEqual(mock_post_save.call_args_list[2][1]['sender'], TestModel1)
        self.assertEqual(mock_post_save.call_args_list[3][0][0],  create_data)
        self.assertEqual(mock_post_save.call_args_list[3][1]['sender'], TestModel2)

        # call_args_list contains all call records so test here to check
        # delete_data have been called with expected four models. Order of
        # model(TestModel3, TestModel4 etc...) varies depand on
        # order of app appears on INSTALLED_APPS
        self.assertEqual(mock_post_delete.call_args_list[0][0][0],  delete_data)
        self.assertEqual(mock_post_delete.call_args_list[0][1]['sender'], TestModel3)
        self.assertEqual(mock_post_delete.call_args_list[1][0][0],  delete_data)
        self.assertEqual(mock_post_delete.call_args_list[1][1]['sender'], TestModel4)
        self.assertEqual(mock_post_delete.call_args_list[2][0][0],  delete_data)
        self.assertEqual(mock_post_delete.call_args_list[2][1]['sender'], TestModel1)
        self.assertEqual(mock_post_delete.call_args_list[3][0][0],  delete_data)
        self.assertEqual(mock_post_delete.call_args_list[3][1]['sender'], TestModel2)
