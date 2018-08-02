from django.apps import apps

from haystack.backends.elasticsearch2_backend import Elasticsearch2SearchEngine
from haystack.utils.loading import UnifiedIndex


class InternalSearchUnifiedIndex(UnifiedIndex):

    def collect_indexes(self):
        indexes = []
        internalsearch_config = apps.get_app_config('djangocms_internalsearch')
        config_list = internalsearch_config.cms_extension.internalsearch_apps_config
        import ipdb
        ipdb.set_trace()
        for item in config_list:
            import ipdb
            ipdb.set_trace()

            if getattr(item, 'haystack_use_for_indexing', False) and getattr(item, 'get_model', None):

                class_path = "%s.internal_search.%s" % ('djangocms_internalsearch', item.__name__)

                if class_path in self.excluded_indexes or self.excluded_indexes_ids.get(item_name) == id(item):
                    index_name = item.model.__name__ + 'Index'
                    self.excluded_indexes_ids[str(index_name)] = id(item)
                    continue

                indexes.append(item())
        return indexes


class InternalSearchESEngine(Elasticsearch2SearchEngine):
    unified_index = InternalSearchUnifiedIndex
