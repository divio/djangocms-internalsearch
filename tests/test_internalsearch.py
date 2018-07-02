from importlib import import_module
from mock import patch, Mock


from django.test import override_settings
from django.apps import apps, AppConfig
from django.core.exceptions import ImproperlyConfigured

from cms import app_registration
from cms.app_registration import get_cms_extension_apps, get_cms_config_apps
# from djangocms_internalsearch.cms_config import CMSCoreExtensions
from djangocms_internalsearch.cms_config import InternalSearchCMSExtension
# from cms.apps import CMSConfig
# from cms.utils import setup
from cms.test_utils.testcases import CMSTestCase
from cms.utils.setup import setup_cms_apps

# from djangocms_internalsearch.test_utils.project.app_with_cms_config.models import TestModel

class AutodiscoverTestCase(CMSTestCase):

    @override_settings(INSTALLED_APPS=[
        'djangocms_internalsearch',
        'djangocms_internalsearch.test_utils.app_with_cms_config',
    ])
    def test_cms_config(self):
        app_registration.autodiscover_cms_configs()

        import pdb; pdb.set_trace()
        extensions = InternalSearchCMSExtension()
        app = apps.get_app_config('app_with_cms_config')
        # cms_config = Mock(
        #     djangocms_internalsearch_enabled=True,
        #     internalsearch_models=['TestModel',],
        #     app_config=Mock(
        #         label='app_with_cms_config'
        #     )
        # )
        # extensions.configure_app(cms_config)

#
# class ConfigureWizardsIntegrationTestCase(CMSTestCase):
#
#     def setUp(self):
#         # The results of get_cms_extension_apps and get_cms_config_apps
#         # are cached. Clear this cache because installed apps change
#         # between tests and therefore unlike in a live environment,
#         # results of this function can change between tests
#         get_cms_extension_apps.cache_clear()
#         get_cms_config_apps.cache_clear()
#
#     @override_settings(INSTALLED_APPS=[
#         'djangocms_internalsearch',
#         'app_with_cms_config',
#     ])
#     def test_adds_internalsearch_to_dict(self):
#         setup_cms_apps()
#
#
#         # import pdb
#         # pdb.set_trace()
