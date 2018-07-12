from haystack import indexes
from cms.models import CMSPlugin, Page
from .search_util import create_search_index_for_haystack

'''
class PageSearchIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True)

    def get_model(self):
        return Page
'''

this_mod = globals()


def gen_classes():
    class Meta:
        model = Page

    def prepare_text(self, obj):
        return "{}".format(obj.changed_by)

    klass_name = 'PageIndex'
    klass = type(klass_name, (indexes.ModelSearchIndex, indexes.Indexable),
                 {'prepare_text': prepare_text, 'Meta': Meta})

    def klass__init(self, extra_field_kwargs=None):
        super(klass, self).__init__()
        self.text.use_template = False

    setattr(klass, "__init__", klass__init)
    this_mod[klass_name] = klass


# generate the classes when the module is loaded
gen_classes()



