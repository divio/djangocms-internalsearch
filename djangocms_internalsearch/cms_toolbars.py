from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

@toolbar_pool.register
class InternalSearchToolbar(CMSToolbar):

    def populate(self):
        # url = reverse('search')
        menu = self.toolbar.add_button('Internal search', '/admin/djangocms_internalsearch')
        # menu.add_sideframe_item(_('Page Template Search'), url=url)
        # menu.add_sideframe_item(_('Plugin Search'), url='#')
