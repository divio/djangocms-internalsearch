from __future__ import generators
import sys
from functools import partial
from haystack import indexes
from django.core.exceptions import ImproperlyConfigured

from djangocms_internalsearch import cms_config


def create_search_index_for_haystack(self):

    model_list = cms_config.InternalSearchCMSExtension().internalsearch_models

    if not model_list:
        raise ImproperlyConfigured(
            "internal search expect models, got none")
    else:
        for model in model_list:
            class_created = class_factory(model + 'SearchIndex')
            class_created.get_class_model = partial(get_class_model(model), class_created)


class BaseClass(indexes.SearchIndex, indexes.Indexable):
    def __init__(self, class_type):
        self._type = class_type


def class_factory(name, BaseClass=BaseClass):
    def __init__(self):
        BaseClass.__init__(self, name)

    new_class = type(name, (BaseClass,), {"__init__": __init__})

    return new_class


def get_class_model(model_name):
    return getattr(sys.modules[__name__], model_name)

