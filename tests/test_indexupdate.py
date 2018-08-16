from django.template import engines

from cms.api import add_plugin
from cms.models import CMSPlugin, Title
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from haystack.query import SearchQuerySet

from tests.utils import BaseTestCase

from djangocms_internalsearch.helpers import save_to_index
from djangocms_internalsearch.internal_search import PageContentConfig


def template_from_string(value):
    """Create an engine-specific template based on provided string.
    """
    return engines.all()[0].from_string(value)


class NotIndexedPlugin(CMSPluginBase):
    model = CMSPlugin
    plugin_content = 'rendered plugin content'
    render_template = template_from_string(plugin_content)

    def render(self, context, instance, placeholder):
        return context


plugin_pool.register_plugin(NotIndexedPlugin)


class UpdateIndexTestCase(BaseTestCase):

    def setUp(self):
        self.index = PageContentConfig()
        self.request = None
        self.token = None

    def test_add_page_to_update_index(self):
        kwargs = {'obj': self.pg1}
        operation = 'add_page_translation'
        save_to_index(Title, operation, self.request, self.token, **kwargs)

        title_obj = Title.objects.get(pk=self.pg1.title_set.all()[0].pk)
        self.assertEqual(1, SearchQuerySet().models(Title).filter(id=title_obj.pk).count())

    def test_delete_page_from_index(self):
        kwargs = {'obj': self.pg1}
        operation = 'delete_page'
        save_to_index(Title, operation, self.request, self.token, **kwargs)

        title_obj = Title.objects.get(pk=self.pg1.title_set.all()[0].pk)
        self.assertEqual(0, SearchQuerySet().models(Title).filter(id=title_obj.pk).count())

    def test_add_plugin_to_update_index(self):

        plugin = add_plugin(self.pg1.get_placeholders('en')[0], NotIndexedPlugin, 'en')
        kwargs = {'placeholder': self.pg1.get_placeholders('en')[0]}
        operation = 'add_plugin'
        save_to_index(Title, operation, self.request, self.token, **kwargs)

        self.assertEqual(1, plugin.id)
