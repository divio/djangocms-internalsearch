from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse  # noqa: F401


@toolbar_pool.register
class InternalSearchToolbar(CMSToolbar):
    """
    Adding button to CMS toolbar to access plugin admin area
    """

    def populate(self):
        # TODO: make url dynamic
        self.toolbar.add_button('Internal search', '/admin/djangocms_internalsearch')
