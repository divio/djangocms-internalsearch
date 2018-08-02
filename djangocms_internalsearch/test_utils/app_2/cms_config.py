from cms.app_base import CMSAppConfig

from djangocms_internalsearch.base import BaseSearchConfig

from .models import TestModel1, TestModel2


class TestModel1Config(BaseSearchConfig):
    model = TestModel1
    list_display = ['field1', 'field2']

    def prepare_text(self, obj):
        return "Lorem ipsum..."


class TestModel2Config(BaseSearchConfig):
    model = TestModel2
    list_display = ['field1', 'field2']

    def prepare_text(self, obj):
        return "Lorem ipsum..."


class CMSApp2Config(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_config_list = [TestModel1Config, TestModel2Config]
