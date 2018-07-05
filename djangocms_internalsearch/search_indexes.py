import datetime
from haystack import indexes
from cms.models import CMSPlugin
from django.contrib.auth.models import User
from django.db import models
from haystack import signals


class CMSPluginIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #placeholder = indexes.CharField(model_attr='placeholder')
    #parent = indexes.CharField(model_attr='parent')
    #position = indexes.CharField(model_attr='position')
    #language = indexes.CharField(model_attr='language')
    plugin_type = indexes.CharField(model_attr='plugin_type')
    #creation_date = indexes.DateTimeField(model_attr='creation_date')
    #changed_date = indexes.DateTimeField(model_attr='changed_date')

    #rendered = indexes.CharField(use_template=True, indexed=False)


    def get_model(self):
        import pdb;pdb.set_trace()
        return CMSPlugin


