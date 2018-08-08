# import copy
#
# from haystack.exceptions import NotHandled
# from haystack.signals import (
#     RealtimeSignalProcessor as BaseRealtimeSignalProcessor
# )
#
# from .signals import add_to_index
#
#
# class RealtimeSignalProcessor(BaseRealtimeSignalProcessor):
#
#     def setup(self):
#         super(RealtimeSignalProcessor, self).setup()
#         add_to_index.connect(self.handle_save)
#
#     def teardown(self):
#         super(RealtimeSignalProcessor, self).teardown()
#         add_to_index.disconnect(self.handle_save)
#
#     def handle_save(self, sender, instance, **kwargs):
#         kwargs = copy.copy(kwargs)
#
#         using_backends = self.connection_router.for_write(instance=instance)
#
#         for using in using_backends:
#             kwargs['using'] = using
#
#             try:
#                 index = self.connections[using].get_unified_index().get_index(sender)
#                 index.update_object(instance, **kwargs)
#             except NotHandled:
#                 pass
