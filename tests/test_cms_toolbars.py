from django.contrib.auth.models import Permission
from django.test.client import RequestFactory

from cms.middleware.toolbar import ToolbarMiddleware
from cms.test_utils.testcases import CMSTestCase
from cms.toolbar.items import SideframeButton
from cms.toolbar.toolbar import CMSToolbar

from djangocms_internalsearch.cms_toolbars import InternalSearchToolbar


class CMSToolbarsTestCase(CMSTestCase):
    def _get_page_request(self, page, user):
        request = RequestFactory().get("/")
        request.session = {}
        request.user = user
        request.current_page = page
        mid = ToolbarMiddleware()
        mid.process_request(request)
        if hasattr(request, "toolbar"):
            request.toolbar.populate()
        return request

    def _get_toolbar(self, content_obj, user, **kwargs):
        """Helper method to set up the toolbar
        """
        request = self._get_page_request(
            page=content_obj.page if content_obj else None, user=user
        )
        cms_toolbar = CMSToolbar(request)
        toolbar = InternalSearchToolbar(
            cms_toolbar.request, toolbar=cms_toolbar, is_current_app=True, app_path="/"
        )
        toolbar.toolbar.set_object(content_obj)

        return toolbar

    def test_cms_toolbar_has_internal_search_button(self):
        user = self.get_standard_user()
        user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="djangocms_internalsearch",
                codename="change_internalsearchproxy",
            )
        )
        toolbar = self._get_toolbar(None, user=user, edit_mode=True)
        toolbar.populate()
        toolbar.post_template_populate()
        self.assertIsInstance(
            toolbar.toolbar.left_items[-1].buttons[0], SideframeButton
        )
        self.assertEqual(
            toolbar.toolbar.left_items[-1].buttons[0].name, "Internal search"
        )

    def test_cms_toolbar_button_not_shown_if_no_permission(self):
        user = self.get_standard_user()
        toolbar = self._get_toolbar(None, user=user, edit_mode=True)
        toolbar.populate()
        toolbar.post_template_populate()
        self.assertFalse(toolbar.toolbar.left_items)
