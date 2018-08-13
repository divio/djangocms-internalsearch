from django.contrib.admin.sites import AdminSite

from djangocms_internalsearch.admin import IntenalSearchAdmin
from djangocms_internalsearch.filters import (
    AuthorFilter,
    LanguageFilter,
    VersionStateFilter,
)
from djangocms_internalsearch.models import InternalSearchProxy

from .utils import TestCase


class MockRequest:
    pass


request = MockRequest()


class InternalSearchAdminListing(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.model_admin = IntenalSearchAdmin(InternalSearchProxy, self.site)

    def test_field_arguments(self):
        self.assertEqual(list(self.model_admin.get_list_display(request)),
                         ['id', 'title_link', 'site_name', 'language',
                          'author', 'content_type', 'version_status'])

        self.assertEqual(list(self.model_admin.get_ordering(request)), ['-id', ])
        self.assertEqual(self.model_admin.list_filter, (LanguageFilter, VersionStateFilter, AuthorFilter))
        self.assertEqual(self.model_admin.list_per_page, 15)
        self.assertEqual(self.model_admin.search_fields, ('text', 'title'))
