try:
    from unittest.mock import Mock
except ImportError:
    raise "InternalSearch app requires Python 3.3 or above"

from django.core.exceptions import ImproperlyConfigured

from cms import app_registration
from cms.test_utils.testcases import CMSTestCase

from djangocms_internalsearch.cms_config import InternalSearchCMSExtension
from djangocms_internalsearch.test_utils.app_1_with_search_cms_config.models import (
    TestModel3,
    TestModel4,
)
from djangocms_internalsearch.test_utils.app_2_with_search_cms_config.models import (
    TestModel1,
    TestModel2,
)


class CMSConfigUnitTestCase(CMSTestCase):

    def test_missing_cms_config(self):

        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            app_config=Mock(label='blah_cms_config'))

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)

    def test_invalid_cms_config_parameter(self):

        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            search_models=23234,
            app_config=Mock(label='blah_cms_config'))

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(cms_config)

    def test_valid_cms_config_parameter(self):

        extensions = InternalSearchCMSExtension()

        cms_config = Mock(
            djangocms_internalsearch_enabled=True,
            search_models=[TestModel1, TestModel2, TestModel3, TestModel4],
            app_config=Mock(label='blah_cms_config'))

        extensions.configure_app(cms_config)

        self.assertTrue(TestModel1 in extensions.internalsearch_models)
        self.assertTrue(TestModel2 in extensions.internalsearch_models)
        self.assertTrue(TestModel3 in extensions.internalsearch_models)
        self.assertTrue(TestModel4 in extensions.internalsearch_models)


class CMSConfigIntegrationTestCase(CMSTestCase):

    def setUp(self):
        app_registration.get_cms_extension_apps.cache_clear()
        app_registration.get_cms_config_apps.cache_clear()

    # @patch.object(post_obj_operation, 'connect')
    # @patch.object(post_placeholder_operation, 'connect')
    # def test_integration_with_other_apps(self,
    #                                      mock_post_placeholder_operation,
    #                                      mock_post_obj_operation):
    #     # import ipdb
    #     # ipdb.set_trace()
    #     setup_cms_apps()
    #     # check of howmany mock methods has been call
    #     # Test utils has two apps with two models so expecting
    #     # method to call four times.
    #     self.assertEqual(mock_post_placeholder_operation.call_count, 4)
    #     self.assertEqual(mock_post_obj_operation.call_count, 4)
    #
    #     # call_args_list contains all call records so test here to check
    #     # create_data have been called with expected four models. Order of
    #     # model(TestModel3, TestModel4 etc...) varies depand on
    #     # order of app appears on INSTALLED_APPS
    #     self.assertEqual(mock_post_obj_operation.call_args_list[0][0][0],  update_to_index)
    #     self.assertEqual(mock_post_obj_operation.call_args_list[0][1]['sender'], TestModel3)
    #     self.assertEqual(mock_post_obj_operation.call_args_list[1][0][0],  update_to_index)
    #     self.assertEqual(mock_post_obj_operation.call_args_list[1][1]['sender'], TestModel4)
    #     self.assertEqual(mock_post_obj_operation.call_args_list[2][0][0],  update_to_index)
    #     self.assertEqual(mock_post_obj_operation.call_args_list[2][1]['sender'], TestModel1)
    #     self.assertEqual(mock_post_obj_operation.call_args_list[3][0][0],  update_to_index)
    #     self.assertEqual(mock_post_obj_operation.call_args_list[3][1]['sender'], TestModel2)
    #
    #     # call_args_list contains all call records so test here to check
    #     # delete_data have been called with expected four models. Order of
    #     # model(TestModel3, TestModel4 etc...) varies depand on
    #     # order of app appears on INSTALLED_APPS
    #     self.assertEqual(
    #         mock_post_placeholder_operation.call_args_list[0][0][0],  remove_from_index)
    #     self.assertEqual(
    #         mock_post_placeholder_operation.call_args_list[0][1]['sender'], TestModel3)
    #     self.assertEqual(
    #         mock_post_placeholder_operation.call_args_list[1][0][0],  remove_from_index)
    #     self.assertEqual(
    #         mock_post_placeholder_operation.call_args_list[1][1]['sender'], TestModel4)
    #     self.assertEqual(
    #         mock_post_placeholder_operation.call_args_list[2][0][0],  remove_from_index)
    #     self.assertEqual(
    #         mock_post_placeholder_operation.call_args_list[2][1]['sender'], TestModel1)
    #     self.assertEqual(
    #         mock_post_placeholder_operation.call_args_list[3][0][0],  remove_from_index)
    #     self.assertEqual(
    #         mock_post_placeholder_operation.call_args_list[3][1]['sender'], TestModel2)
