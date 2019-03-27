from django.contrib.auth import get_permission_codename
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

from djangocms_internalsearch.models import InternalSearchProxy


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
        opts = InternalSearchProxy._meta
        codename = get_permission_codename("change", opts)
        if not self.request.user.has_perm(
            "{app_label}.{codename}".format(app_label=opts.app_label, codename=codename)
        ):
            return
        self.toolbar.add_sideframe_button(
            _("Internal search"),
            reverse(
                "admin:{app_label}_{model_name}_changelist".format(
                    app_label=opts.app_label, model_name=opts.model_name
                )
            ),
        )
