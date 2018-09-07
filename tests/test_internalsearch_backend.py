from unittest import skipIf

from django.test import TestCase

from haystack.utils import loading

from djangocms_internalsearch.base import BaseSearchConfig
try:
    from djangocms_internalsearch.backends.elasticsearch2 import InternalSearchESEngine
except ImportError:
    InternalSearchESEngine = None

from .utils import inheritors


@skipIf(InternalSearchESEngine is None, "elasticsearch not installed")
class LoadInternalSearchBackendTestCase(TestCase):

    def test_load_internalsearch_elasticsearch(self):
        backend = loading.load_backend(
            "djangocms_internalsearch.backends.elasticsearch2.InternalSearchESEngine"
        )
        self.assertEqual(backend.__name__, "InternalSearchESEngine")


@skipIf(InternalSearchESEngine is None, "elasticsearch not installed")
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
