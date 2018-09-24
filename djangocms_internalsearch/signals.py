from django.dispatch import Signal

content_object_change_signal = Signal(
    providing_args=[
        "content_object",
    ]
)


