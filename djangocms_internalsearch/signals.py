from django.dispatch import Signal

page_content_change_signal = Signal(
    providing_args=[
        "page_content_object",
    ]
)


