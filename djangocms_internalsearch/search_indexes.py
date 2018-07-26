import inspect
from collections import Iterable

from haystack import indexes


def create_indexes(model_list):
    """
    The below creates classes for haystack to index particular
    model which we have passed in our apps.py file.
    """
    if not isinstance(model_list, Iterable):
        raise TypeError("Generate method expects a list or tuple")

    for model in model_list:
        if not inspect.isclass(model):
            raise TypeError("Model is not a class object")

        class_name = model.__name__ + 'Index'
        search_index_class = class_factory(class_name, model)

        globals()[class_name] = search_index_class

        if not inspect.isclass(search_index_class):
            raise TypeError("Created search index is not a class")


def class_factory(name, model):
    text = indexes.CharField(document=True)

    # TODO; need to add custom fields for models

    def get_model(self):
        return model

    index_class_dict = {"text": text, "get_model": get_model}
    new_class = type(name,
                     (indexes.SearchIndex, indexes.Indexable),
                     index_class_dict
                     )
    return new_class
