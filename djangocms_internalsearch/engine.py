from haystack.backends import BaseEngine, elasticsearch_backend
from haystack.utils.loading import UnifiedIndex


class InternalSearchEngine(BaseEngine):

    backend = elasticsearch_backend.ElasticsearchSearchBackend
    query = elasticsearch_backend.ElasticsearchSearchQuery

    def __init__(self, excluded_indexes=None):
        self._indexes = {}

    def get_unified_index(self):
        return self._indexes
