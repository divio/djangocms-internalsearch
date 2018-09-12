from haystack.backends.elasticsearch2_backend import Elasticsearch2SearchEngine

from ..unified_index import InternalSearchUnifiedIndex


class InternalSearchESEngine(Elasticsearch2SearchEngine):
    unified_index = InternalSearchUnifiedIndex
