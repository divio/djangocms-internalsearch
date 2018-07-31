from abc import ABC, abstractmethod


class BaseConfig(ABC):
    """
    Base config class to provide list of attributes that sub class must provide
    """
    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError("Config class must provide model")

    @property
    @abstractmethod
    def fields(self):
        raise NotImplementedError("Config class must provide fields to index")

    @property
    @abstractmethod
    def list_display(self):
        raise NotImplementedError("Config class must provide list_display fields")

    @property
    @abstractmethod
    def index(self):
        raise NotImplementedError(
            "Config class must provide index attributes. Assign None to auto generate")
