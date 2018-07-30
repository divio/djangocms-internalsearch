from haystack.backends import BaseEngine, elasticsearch_backend
from haystack.utils.loading import UnifiedIndex


class InternalSearchEngine(BaseEngine):

    backend = elasticsearch_backend.ElasticsearchSearchBackend
    query = elasticsearch_backend.ElasticsearchSearchQuery
    unified_index = UnifiedIndex()

    def get_unified_index(self):
        if self._index is None:
            self._index = self.unified_index(self.options.get('EXCLUDED_INDEXES', []))

        return self._index
