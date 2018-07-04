from django.contrib.auth.models import User
from django.test import TestCase

from cms.api import create_page


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create pages
        cls.pg1 = create_page(title='Page 1', template='page.html', language='en',)
        # create users, groups and roles
        cls.user = User.objects.create_superuser(
            username='test', email='test@test.com', password='test',)


class BaseViewTestCase(BaseTestCase):

    def setUp(self):
        self.client.force_login(self.user)
