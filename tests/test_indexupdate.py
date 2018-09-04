from cms.models import Title
from cms.operations import ADD_PAGE_TRANSLATION, DELETE_PAGE

from haystack import connections
from haystack.utils.loading import UnifiedIndex
from tests.utils import BaseTestCase

from djangocms_internalsearch.helpers import save_to_index
from djangocms_internalsearch.internal_search import (
    PageContentConfig,
    get_request,
)


class UpdateIndexTestCase(BaseTestCase):

    def setUp(self):
        super(UpdateIndexTestCase, self).setUp()

        self.unified_index = UnifiedIndex()
        self.wmmi = PageContentConfig()
        self.unified_index.build(indexes=[self.wmmi])
        connections["default"]._index = self.unified_index

        self.sb = connections["default"].get_backend()
        self.sb.setup()

        self.request = get_request(language='en')
        self.token = None

    def test_add_page_to_update_index(self):
        kwargs = {'obj': self.pg1}
        save_to_index(Title, ADD_PAGE_TRANSLATION, self.request, self.token, **kwargs)
        self.assertEqual(1, self.sb.index.doc_count())

    def test_delete_page_from_index(self):
        kwargs = {'obj': self.pg1}
        save_to_index(Title, ADD_PAGE_TRANSLATION, self.request, self.token, **kwargs)
        self.assertEqual(1, self.sb.index.doc_count())
        kwargs = {'obj': self.pg1}
        save_to_index(Title, DELETE_PAGE, self.request, self.token, **kwargs)
        self.assertEqual(0, self.sb.index.doc_count())
