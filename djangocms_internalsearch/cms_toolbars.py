from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


@toolbar_pool.register
class InternalSearchToolbar(CMSToolbar):
    """
    Adding button to CMS toolbar to access plugin admin area
    """

    def populate(self):
        #TODO: make url dynamic 
        menu = self.toolbar.add_button('Internal search',
                                       '/admin/djangocms_internalsearch')
