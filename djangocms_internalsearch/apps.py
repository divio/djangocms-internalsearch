from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .helpers import save_to_index, page_content_change_receiver


class InternalsearchConfig(AppConfig):
    name = 'djangocms_internalsearch'
    verbose_name = _('django CMS Internal Search')

    def ready(self):
        from cms.signals import (
            post_obj_operation,
            post_placeholder_operation
        )
        from .signals import page_content_change_signal

        page_content_change_signal.connect(page_content_change_receiver)
        post_obj_operation.connect(save_to_index)
        post_placeholder_operation.connect(save_to_index)
