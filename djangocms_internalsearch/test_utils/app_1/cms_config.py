from cms.app_base import CMSAppConfig

from .models import TestModel3, TestModel4


class TestModel3Config:
    model = TestModel3
    fields = ['field1', 'field2']


class TestModel4Config:
    model = TestModel4
    fields = ['field1', 'field2']


class CMSApp1Config(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_config_list = [TestModel3Config, TestModel4Config]
