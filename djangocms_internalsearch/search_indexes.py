from haystack import indexes
from .models import (
    QueryProxy,
)

"""
If we don't register the class below things still work but we get the following warning

/lib/python3.5/site-packages/haystack/query.py:373: UserWarning: The model <class 'djangocms_internalsearch.models.QueryProxy'> is not registered for search.
  warnings.warn('The model %r is not registered for search.' % (model,))
"""
class QueryProxyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    achar = indexes.CharField(model_attr='achar')
    aint = indexes.IntegerField(model_attr='aint')

    def get_model(self):
        return QueryProxy

    def prepare_text(self, obj):
        t = '{}'.format(obj.achar)
        return t
