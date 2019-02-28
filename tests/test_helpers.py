from unittest import skipUnless

from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase

from tests.utils import is_versioning_enabled


if is_versioning_enabled():
    from djangocms_internalsearch import helpers
    from djangocms_internalsearch.test_utils import factories
    from djangocms_versioning.models import Version
    from djangocms_versioning.constants import DRAFT


@skipUnless(is_versioning_enabled(), "Test only relevant for versioning")
class UpdateIndexTestCase(CMSTestCase):
    def test_get_all_versions(self):

        user = factories.UserFactory(
            username="test_versions",
            email="test_versions@test.com",
            password="test_versions",
            is_staff=True,
            is_superuser=True,
        )

        pg = create_page(
            title="Page with versions",
            template="INHERIT",
            language="en",
            created_by=user,
        )
        v1 = Version.objects.filter_by_grouper(pg).filter(state=DRAFT).first()
        v1.publish(user)
        v1.unpublish(user)
        v2 = v1.copy(user)

        versions = helpers.get_all_versions(v2.content)
        self.assertTrue(len(versions), 2)
