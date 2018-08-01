from haystack.backends import BaseEngine
from haystack.utils.loading import UnifiedIndex


class ISearchUnifiedIndex(UnifiedIndex):

    def collect_indexes(self):
        return self._indexes


class ISearchESEngine(BaseEngine):

    unified_index = ISearchUnifiedIndex

    # def get_unified_index(self):
    #     return self._indexes
