from unittest import skipUnless

from cms.test_utils.testcases import CMSTestCase

from tests.utils import is_versioning_enabled

from djangocms_internalsearch.contrib.cms.internal_search import (
    annotated_pagecontent_queryset,
)


if is_versioning_enabled():
    from djangocms_internalsearch.test_utils import factories


@skipUnless(is_versioning_enabled(), 'Test only relevant for versioning')
class CmsInternalSearchTestCase(CMSTestCase):

    def test_annotated_pagecontent_queryset(self):
        language1 = 'en'
        language2 = 'de'
        page1 = factories.PageFactory()
        page2 = factories.PageFactory()

        page1_version1 = factories.PageVersionFactory(
            content__page=page1, content__language=language1)
        page2_version1 = factories.PageVersionFactory(
            content__page=page2, content__language=language2)
        page1_version2 = factories.PageVersionFactory(
            content__page=page1, content__language=language1)

        qs = annotated_pagecontent_queryset()
        self.assertEqual(
            {obj.pk: obj.latest_pk for obj in qs},
            {
                page1_version1.pk: page1_version2.pk,
                page2_version1.pk: page2_version1.pk,
                page1_version2.pk: page1_version2.pk
            },
        )
