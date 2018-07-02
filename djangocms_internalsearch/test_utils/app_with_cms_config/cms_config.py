from cms.app_base import CMSAppConfig
# from .models import Model1, Model2

class CMSConfigConfig(CMSAppConfig):
    djangocms_internalsearch_enabled = True
    internalsearch_models = ['TestModel']
