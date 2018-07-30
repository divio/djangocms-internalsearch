from haystack import indexes


def create_indexes(model_list):
    """
    The below creates classes for haystack to index particular
    model which we have passed in our apps.py file.
    """

    for model in model_list:

        class_name = model.__name__ + 'Index'
        search_index_class = class_factory(class_name, model)

        globals()[class_name] = search_index_class


def class_factory(name, model):
    text = indexes.CharField(document=True)

    # TODO; need to add custom fields for models

    def get_model(self):
        return model

    index_class_dict = {"text": text, "get_model": get_model}
    new_class = type(
        name,
        (indexes.SearchIndex, indexes.Indexable),
        index_class_dict
    )

    return new_class
