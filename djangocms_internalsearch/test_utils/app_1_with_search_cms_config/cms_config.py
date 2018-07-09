from cms.app_base import CMSAppConfig

from .models import TestModel3, TestModel4


class CMSApp1Config(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    search_models = [TestModel3, TestModel4]
