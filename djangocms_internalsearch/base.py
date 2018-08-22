from haystack import indexes


class BaseSearchConfig(indexes.SearchIndex, indexes.Indexable):
    """
    Base config class to provide list of attributes that sub class must provide
    """
    text = indexes.NgramField(document=True, use_template=False)

    # admin setting
    list_per_page = 50

    @property
    def model(self):
        raise NotImplementedError("Config class must provide model attribute")

    @property
    def list_display(self):
        raise NotImplementedError("Config class must provide list_display fields")

    def get_model(self):
        return self.model

    def prepare_text(self, obj):
        raise NotImplementedError("Config class must provide prepare_text method for index")
