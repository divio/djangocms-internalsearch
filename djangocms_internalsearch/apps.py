from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .helpers import (
    content_object_delete_receiver,
    content_object_state_change_receiver,
    remove_from_index,
    save_to_index,
)


class InternalsearchConfig(AppConfig):
    name = 'djangocms_internalsearch'
    verbose_name = _('django CMS Internal Search')

    def ready(self):
        from cms.signals import (
            post_obj_operation,
            post_placeholder_operation,
            pre_obj_operation,
        )
        from .signals import content_object_state_change, content_object_delete

        pre_obj_operation.connect(remove_from_index)
        post_obj_operation.connect(save_to_index)
        post_placeholder_operation.connect(save_to_index)

        # listen for object content version changes, delete
        content_object_state_change.connect(content_object_state_change_receiver)
        content_object_delete.connect(content_object_delete_receiver)
