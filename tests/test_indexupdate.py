from cms.models import Title
from cms.operations import ADD_PAGE_TRANSLATION, DELETE_PAGE

from haystack import connections
from haystack.utils.loading import UnifiedIndex
from tests.utils import BaseTestCase

from djangocms_internalsearch.helpers import save_to_index
from djangocms_internalsearch.internal_search import PageContentConfig


class UpdateIndexTestCase(BaseTestCase):

    def setUp(self):
        super(UpdateIndexTestCase, self).setUp()

        self.ui = UnifiedIndex()
        self.wmmi = PageContentConfig()
        self.ui.build(indexes=[self.wmmi])
        connections["default"]._index = self.ui

        self.sb = connections["default"].get_backend()
        self.sb.setup()

        self.request = None
        self.token = None

    def test_add_page_to_update_index(self):
        kwargs = {'obj': self.pg1}
        operation = ADD_PAGE_TRANSLATION
        save_to_index(Title, operation, self.request, self.token, **kwargs)
        self.assertEqual(1, self.sb.index.doc_count())

    def test_delete_page_from_index(self):
        kwargs = {'obj': self.pg1}
        operation = ADD_PAGE_TRANSLATION
        save_to_index(Title, operation, self.request, self.token, **kwargs)
        self.assertEqual(1, self.sb.index.doc_count())
        kwargs = {'obj': self.pg1}
        operation = DELETE_PAGE
        save_to_index(Title, operation, self.request, self.token, **kwargs)
        self.assertEqual(0, self.sb.index.doc_count())
