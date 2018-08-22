from django.test import TestCase

from haystack.utils import loading

from djangocms_internalsearch.base import BaseSearchConfig
from djangocms_internalsearch.engine import InternalSearchESEngine
from djangocms_internalsearch.internal_search import (
    FilerConfig,
    ImageConfig,
    PageContentConfig,
)
from djangocms_internalsearch.test_utils.app_1.cms_config import (
    TestModel3Config,
    TestModel4Config,
)
from djangocms_internalsearch.test_utils.app_2.cms_config import (
    TestModel1Config,
    TestModel2Config,
)


class LoadInternalSearchBackendTestCase(TestCase):

    def test_load_internalsearch_elasticsearch(self):
        backend = loading.load_backend(
            "djangocms_internalsearch.engine.InternalSearchESEngine"
        )
        self.assertEqual(backend.__name__, "InternalSearchESEngine")


class SearchIndexTestCase(TestCase):

    def setUp(self):
        self.unified_index = InternalSearchESEngine.unified_index()
        self.indexes = self.unified_index.collect_indexes()

    def test_model_indexes(self):
        expected_indexes = [
            TestModel1Config,
            TestModel2Config,
            TestModel3Config,
            TestModel4Config,
            PageContentConfig,
            ImageConfig,
            FilerConfig,
        ]
        for config_obj in self.indexes:
            self.assertIsInstance(config_obj, BaseSearchConfig)
            self.assertTrue(type(config_obj) in expected_indexes)
        self.assertTrue(len(self.indexes), len(expected_indexes))
