from django.dispatch import Signal


content_object_state_change = Signal(
    providing_args=[
        "content_object",
        "created",
    ]
)

content_object_delete = Signal(
    providing_args=[
        "content_object",
    ]
)
