from __future__ import generators
import sys
from functools import partial
from haystack import indexes, connections
from haystack.constants import DEFAULT_ALIAS

from django.core.exceptions import ImproperlyConfigured

from djangocms_internalsearch import cms_config
from cms.models import CMSPlugin, Page
from cms.models import pluginmodel



def create_search_index_for_haystack(model_list):


    # #model_list = cms_config.InternalSearchCMSExtension().internalsearch_models
    #
    # if not model_list:
    #     raise ImproperlyConfigured(
    #         "internal search expect models, got none")
    # else:
    #     for model in model_list:
    #         attr_list = [f.name for f in model._meta.get_fields()]
    #         print('attr_list %s' % attÎr_list)
    #         class_created = class_factory(model + 'SearchIndex')
    #         class_created.get_class_model = partial(get_class_model(model), class_created)

    #model_list_local = ['CMSPlugin']

    #the_module = __import__('cms.models', globals(), locals(), [model_list_local[0]])

    #model = model_list_local[0]
    class_created = class_factory('PageSearchIndex')
    import pdb; pdb.set_trace()
    instance_of_factory_class = class_created()
    instance_of_factory_class.text = indexes.CharField(document=True)

    class_created.get_model = partial(get_model('Page'), class_created)
    model_obj = class_created.get_model()
    #connections[DEFAULT_ALIAS]._index = None



    #---working---
    #dup_created = duplicate_class_factory('Meta', class_created)
    #instance_of_dup_class = dup_created()
    #instance_of_dup_class.model = model_obj
    #dup_created.model = model_obj
    #---working---

    #model_fields_list = [f.name for f in model_obj._meta.get_fields()]
    #print('list of fields %s' % model_fields_list)
    #model_field_type = model_obj._meta.get_field(model_fields_list[-1]).get_internal_type()
    #print('model field type %s' % model_field_type)
    #class_created.text = indexes.CharField(document=True)
    #class_created.

    return class_created


class BaseClass(indexes.SearchIndex, indexes.Indexable):
    def __init__(self, class_type):
        self._type = class_type


def class_factory(name, BaseClass=BaseClass):
    def __init__(self):
        BaseClass.__init__(self, name)

    new_class = type(name, (BaseClass,), {"__init__": __init__})


    return new_class


class DuplicateBaseClass():
    def __init__(self, class_type):
        self._type = class_type


def duplicate_class_factory(name, parent,  DuplicateBaseClass=DuplicateBaseClass):
    def __init__(self):
        DuplicateBaseClass.__init__(self, name)

    dup_class = type(name, (DuplicateBaseClass, parent), {"__init__": __init__})
    #dup_class.model = None
    return dup_class


def get_model(model_name):
    return getattr(sys.modules[__name__], model_name)

