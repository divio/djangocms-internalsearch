from tests.utils import BaseTestCase

from haystack import connections
from haystack.utils.loading import UnifiedIndex
from tests.utils import BaseTestCase

from djangocms_internalsearch.contrib.cms.internal_search import (
    PageContentConfig,
)

from test_helpers.pyfrom djangocms_internalsearch import helpers


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

    def test_get_all_versions(self):
        pass
