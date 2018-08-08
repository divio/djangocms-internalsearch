from django.dispatch.dispatcher import Signal

add_to_index = Signal(providing_args=['sender', 'instance'])
