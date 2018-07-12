from haystack import indexes
from cms.models import CMSPlugin, Page
from .search_util import create_search_index_for_haystack

'''
class PageSearchIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True)

    def get_model(self):
        return Page
'''

