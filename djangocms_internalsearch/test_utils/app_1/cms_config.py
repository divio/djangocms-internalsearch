from cms.app_base import CMSAppConfig

from djangocms_internalsearch.base import BaseSearchConfig

from .models import TestModel3, TestModel4


class TestModel3Config(BaseSearchConfig):
    model = TestModel3
    list_display = ['field1', 'field2']

    def prepare_text(self, obj):
        return "Lorem ipsum..."


class TestModel4Config(BaseSearchConfig):
    model = TestModel4
    list_display = ['field1', 'field2']

    def prepare_text(self, obj):
        return "Lorem ipsum..."


class CMSApp1Config(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_config_list = [TestModel3Config, TestModel4Config]
