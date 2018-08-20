from cms.models import Title

from tests.utils import BaseTestCase

from djangocms_internalsearch.helpers import save_to_index
from djangocms_internalsearch.internal_search import PageContentConfig

from haystack import connections
from haystack.utils.loading import UnifiedIndex


class UpdateIndexTestCase(BaseTestCase):

    def setUp(self):
        super(UpdateIndexTestCase, self).setUp()

        self.ui = UnifiedIndex()
        self.wmmi = PageContentConfig()
        self.ui.build(indexes=[self.wmmi])
        connections["default"]._index = self.ui

        self.sb = connections["default"].get_backend()
        connections["default"]._index = self.ui
        self.sb.setup()

        self.request = None
        self.token = None

    def test_add_page_to_update_index(self):
        kwargs = {'obj': self.pg1}
        operation = 'add_page_translation'
        save_to_index(Title, operation, self.request, self.token, **kwargs)

        self.assertEqual(1, self.sb.index.doc_count())

    def test_delete_page_from_index(self):
        kwargs = {'obj': self.pg1}
        operation = 'add_page_translation'
        save_to_index(Title, operation, self.request, self.token, **kwargs)
        self.assertEqual(1, self.sb.index.doc_count())

        kwargs = {'obj': self.pg1}
        operation = 'delete_page'
        save_to_index(Title, operation, self.request, self.token, **kwargs)
        self.assertEqual(0, self.sb.index.doc_count())
