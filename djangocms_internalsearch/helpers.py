
def save_to_index(model):
    # TODO; add/update object
    pass


def render_plugin(plugin, context, renderer=None):
    if renderer:
        content = renderer.render_plugin(
            instance=plugin,
            context=context,
            editable=False,
        )
    else:
        content = plugin.render_plugin(context)
    return content
