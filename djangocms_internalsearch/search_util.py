from haystack import connections
from haystack.constants import DEFAULT_ALIAS

from haystack import indexes

import djangocms_internalsearch.search_indexes as search_index


class GenericSearchIndex():
    model_list = ['CMSPlugin', ]
    '''
    for model in model_list:
        search_index_class_name = "%s_%sSearchIndex"%(model, model)

        setattr(search_index, model, create(model))
    connections[DEFAULT_ALIAS]._index = None

    def create(self, model):
        class DynamicSearchIndex(indexes.SearchIndex, indexes.Indexable):
            def get_model(self):
                return model
        return
    '''


