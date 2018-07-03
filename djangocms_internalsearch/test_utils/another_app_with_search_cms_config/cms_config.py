from cms.app_base import CMSAppConfig


class CMSConfigConfig(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_models = ['TestModel1', 'TestModel2']
