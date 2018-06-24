from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

@toolbar_pool.register
class InternalSearchToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu('internalsearch-app', _('Content Search'))
        url = reverse('search')
        menu.add_sideframe_item(_('Page Template Search'), url=url)
        menu.add_sideframe_item(_('Plugin Search'), url='#')
