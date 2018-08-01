from cms.app_base import CMSAppConfig

from djangocms_internalsearch.base import ISearchBaseConfig

from .models import TestModel1, TestModel2


class TestModel1Config(ISearchBaseConfig):
    model = TestModel1
    fields = ['field1', 'field2']


class TestModel2Config(ISearchBaseConfig):
    model = TestModel2
    fields = ['field1', 'field2']


class CMSApp2Config(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_config_list = [TestModel1Config, TestModel2Config]
