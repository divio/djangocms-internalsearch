from django.contrib.admin.sites import AdminSite

from djangocms_internalsearch.admin import InternalSearchAdmin
from djangocms_internalsearch.contrib.cms.filters import ContentTypeFilter
from djangocms_internalsearch.models import InternalSearchProxy

from .utils import TestCase


class MockRequest:
    pass


request = MockRequest()


class InternalSearchAdminListing(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.model_admin = InternalSearchAdmin(InternalSearchProxy, self.site)

    def test_field_arguments(self):
        self.assertEqual(list(self.model_admin.get_list_display(request)),
                         ['id', 'title', 'slug', 'site_name', 'language',
                          'author', 'content_type', 'version_status'])

        self.assertEqual(list(self.model_admin.get_ordering(request)), ['-id', ])
        self.assertEqual(self.model_admin.list_filter, [ContentTypeFilter, ])
        self.assertEqual(self.model_admin.list_per_page, 100)
        self.assertEqual(self.model_admin.search_fields, ('text', 'title'))
