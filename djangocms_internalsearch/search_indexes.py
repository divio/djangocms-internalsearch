from haystack import indexes

this_mod = globals()

'''
The below creates a class for haystack to index 
particular model which we have passed in our 
apps.py file.
'''


def gen_classes(received_class):

    text = indexes.CharField(document=True)

    def get_model(self):
        return received_class

    def prepare_text(self, obj):
        return "{}".format(obj.plugin_type)

    klass_name = received_class.__name__+'SearchIndex'
    klass_dict = {'text': text, 'get_model': get_model, 'prepare_text': prepare_text}
    klass = type(klass_name, (indexes.SearchIndex, indexes.Indexable), klass_dict)

    def klass__init(self):
        super(klass, self).__init__()

    setattr(klass, "__init__", klass__init)
    this_mod[klass_name] = klass




