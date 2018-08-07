from haystack import indexes
from .models import (
    AllIndex,
)


# class SearchAllIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=False)
#     achar = indexes.CharField(model_attr='achar')
#     aint = indexes.IntegerField(model_attr='aint')
#
#     def get_model(self):
#         return AllIndex
#
#     def prepare_text(self, obj):
#         t = '{}'.format(obj.achar)
#         return t
