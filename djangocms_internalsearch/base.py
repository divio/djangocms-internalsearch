from haystack import indexes


class BaseSearchConfig(indexes.SearchIndex, indexes.Indexable):
    """
    Base config class to provide list of attributes that sub class must provide
    """
    text = indexes.NgramField(document=True, use_template=False)
    content_type = indexes.CharField()

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

    def prepare_content_type(self, obj):
        raise NotImplementedError("Config class must provide content_type method for index")
