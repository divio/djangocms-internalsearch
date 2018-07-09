from cms.app_base import CMSAppConfig

from .models import TestModel1, TestModel2


class CMSApp2Config(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    search_models = [TestModel1, TestModel2]
