from django.test import TestCase

from haystack.utils import loading

from djangocms_internalsearch.base import BaseSearchConfig
from djangocms_internalsearch.engine import InternalSearchESEngine

from .utils import inheritors


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
        expected_indexes = inheritors(BaseSearchConfig)
        for config_obj in self.indexes:
            self.assertIsInstance(config_obj, BaseSearchConfig)
            self.assertTrue(type(config_obj) in expected_indexes)
        self.assertTrue(len(self.indexes), len(expected_indexes))
