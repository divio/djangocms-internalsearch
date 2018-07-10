from __future__ import generators
import sys
from haystack import connections
from haystack.constants import DEFAULT_ALIAS

from haystack import indexes
from cms.models import CMSPlugin


from djangocms_internalsearch.search_indexes import CMSPluginSearchIndex


def reindex_cmsplugin(sender, **kwargs):
    CMSPluginSearchIndex().update_object(kwargs['instance'].CMSPlugin)


class BaseClass(object):
    def __init__(self, class_type):
        self._type = class_type


def class_factory(name, BaseClass=BaseClass):
    def __init__(self):
        BaseClass.__init__(self, name)
    new_class = type(name, (BaseClass,), {"__init__": __init__})
    #new_class.get_model()

    def get_model():
        return getattr(sys.modules[__name__], name)

    return new_class


#def make_get_model(name):
#    def get_model():
#        return name
#    return get_model()


class GenericSearchIndex():
    model_list = ['CMSPlugin', ]

    #for model in model_list:
    #    class_factory(model)

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


