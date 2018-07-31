from __future__ import unicode_literals

from django.apps import AppConfig, apps
from django.utils.translation import ugettext_lazy as _

from .handlers import update_index
from .helpers import create_indexes
from .engine import InternalSearchEngine


class InternalsearchConfig(AppConfig):
    name = 'djangocms_internalsearch'
    verbose_name = _('django CMS Internal Search')

    def ready(self):
        from cms.signals import (
            post_obj_operation,
            post_placeholder_operation
        )

        post_obj_operation.connect(update_index)
        post_placeholder_operation.connect(update_index)

        internalsearch_indexes = InternalSearchEngine()
        internalsearch_config = apps.get_app_config('djangocms_internalsearch')
        model_list = list(
            config.model for config in internalsearch_config.cms_extension.internalsearch_apps_config
        )
        create_indexes(model_list, internalsearch_indexes)
        # import ipdb
        # ipdb.set_trace()
