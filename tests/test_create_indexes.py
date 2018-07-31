from cms import app_registration
from cms.test_utils.testcases import CMSTestCase

from djangocms_internalsearch.helpers import create_indexes
from djangocms_internalsearch.test_utils.app_2.cms_config import (
    TestModel1Config,
    TestModel2Config,
)

from .utils import TestCase


# class ClassFactoryUnitTestCase(TestCase):
#
#     def test_passing_classes(self):
#         test_class_list = [TestModel1Config.model, TestModel2Config.model]
#         create_indexes(test_class_list)
#         from djangocms_internalsearch.search_indexes import TestModel1Index
#         self.assertEqual(TestModel1Index.__name__, 'TestModel1Index')
#

# class InternalSearchIntegrationTestCase(CMSTestCase, TestCase):
#
#     def setUp(self):
#         app_registration.get_cms_extension_apps.cache_clear()
#         app_registration.get_cms_config_apps.cache_clear()
#
#     def test_config_with_two_apps(self):
#         """
#         App initialise should have created search indexes
#         """
#         with self.assertNotRaises(AttributeError):
#             from djangocms_internalsearch import search_indexes
#             search_indexes.TestModel1Index
#             search_indexes.TestModel2Index
#             search_indexes.TestModel3Index
#             search_indexes.TestModel4Index
