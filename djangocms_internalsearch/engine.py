from django.apps import apps

from haystack.backends.elasticsearch2_backend import Elasticsearch2SearchEngine
from haystack.backends.whoosh_backend import WhooshEngine
from haystack.utils.loading import UnifiedIndex


class InternalSearchUnifiedIndex(UnifiedIndex):

    def collect_indexes(self):
        indexes = []
        internalsearch_config = apps.get_app_config('djangocms_internalsearch')
        apps_config = internalsearch_config.cms_extension.internalsearch_apps_config

        for item in apps_config:
            item_name = item.__name__
            if item.haystack_use_for_indexing:
                class_path = "{}.{}".format(item.__module__, item_name)
                if class_path in self.excluded_indexes or self.excluded_indexes_ids.get(item_name) == id(item):
                    self.excluded_indexes_ids[str(item_name)] = id(item)
                    continue
                indexes.append(item())
        return indexes


class InternalSearchESEngine(Elasticsearch2SearchEngine):
    unified_index = InternalSearchUnifiedIndex


class InternalSearchWhooshEngine(WhooshEngine):
    unified_index = InternalSearchUnifiedIndex
