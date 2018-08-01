from haystack import indexes

from .engine import InternalSearchEngine


def save_to_index(model):
    # TODO; add/update object
    pass


def create_indexes(model_list):
    """
    Prepare attributes to create class
    """
    for model in model_list:
        class_name = model.__name__ + 'Index'
        search_index_class = class_factory(class_name, model)
        InternalSearchEngine.indexes[model] = search_index_class


def class_factory(name, model):
    text = indexes.CharField(document=True)
    # TODO; need to add custom fields for models

    def get_model(self):
        return model

    index_class_dict = {"text": text, "get_model": get_model}
    new_class = type(
        name,
        (indexes.SearchIndex, indexes.Indexable),
        index_class_dict,
    )
    return new_class
