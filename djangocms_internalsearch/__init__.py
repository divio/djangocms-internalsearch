__version__ = '0.0.0'

default_app_config = 'djangocms_internalsearch.apps.InternalsearchConfig'


class BaseConfig(object):
    """
    Base config class to provide interface
    """
    @property
    def model(self):
        raise NotImplementedError

    @property
    def fields(self):
        raise NotImplementedError

    @property
    def list_display(self):
        raise NotImplementedError

    @property
    def index(self):
        """
        set None to auto generate or provide custom index class
        """
        raise NotImplementedError
