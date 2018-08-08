from django.dispatch.dispatcher import receiver

from cms.signals import post_obj_operation

from .signals import add_to_index


@receiver(post_obj_operation)
def save_cms_page(sender, **kwargs):
    inst = kwargs['obj']
    add_to_index.send(sender=sender, instance=inst)
