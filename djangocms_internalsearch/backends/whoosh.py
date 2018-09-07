from haystack.backends.whoosh_backend import WhooshEngine

from ..unified_index import InternalSearchUnifiedIndex


class InternalSearchWhooshEngine(WhooshEngine):
    unified_index = InternalSearchUnifiedIndex
