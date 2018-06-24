from django.contrib.auth.models import User, Group
from django.test import TestCase

from cms.api import create_page

from djangocms_internalsearch.models import Workflow, Role, PageInternalsearchRequest
from djangocms_internalsearch import constants


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        # create pages
        cls.pg1 = create_page(title='Page 1', template='page.html', language='en',)

        # create users, groups and roles
        cls.user = User.objects.create_superuser(
            username='test', email='test@test.com', password='test',)

        cls.role1 = Role.objects.create(name='Role 1', user=cls.user,)


class BaseViewTestCase(BaseTestCase):

    def setUp(self):
        self.client.force_login(self.user)
