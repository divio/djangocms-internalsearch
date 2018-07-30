from abc import ABC, abstractproperty

__version__ = '0.0.0'

default_app_config = 'djangocms_internalsearch.apps.InternalsearchConfig'


class BaseConfig(ABC):
    """
    Base config class to provide list of attributes that sub class must provide
    """
    @property
    @abstractproperty
    def model(self):
        raise NotImplementedError("Config class must provide model")

    @property
    @abstractproperty
    def fields(self):
        raise NotImplementedError("Config class must provide fields to index")

    @property
    @abstractproperty
    def list_display(self):
        raise NotImplementedError("Config class must provide list_display fields")

    @property
    @abstractproperty
    def index(self):
        raise NotImplementedError(
            "Config class must provide index attributes. Assign None to auto generate")
