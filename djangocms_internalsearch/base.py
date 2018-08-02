from abc import abstractmethod

from haystack import indexes


class BaseSearchConfig(indexes.SearchIndex, indexes.Indexable):
    """
    Base config class to provide list of attributes that sub class must provide
    """
    text = indexes.NgramField(document=True, use_template=False)
    content_type = indexes.CharField()

    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError("Config class must provide model attribute")

    @property
    @abstractmethod
    def list_display(self):
        raise NotImplementedError("Config class must provide list_display fields")

    def get_model(self):
        self.model

    @abstractmethod
    def prepare_text(self, obj):
        raise NotImplementedError("Config class must provide prepare_text method for index")

    @abstractmethod
    def prepare_content_type(self, obj):
        raise NotImplementedError("Config class must provide content_type method for index")
