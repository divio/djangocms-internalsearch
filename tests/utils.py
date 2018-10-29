import unittest
from contextlib import contextmanager

from django.apps import apps
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


class TestCase(unittest.TestCase):

    @contextmanager
    def assertNotRaises(self, exc_type):
        try:
            yield None
        except exc_type:
            raise self.failureException('{} raised'.format(exc_type.__name__))


def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


def is_versioning_enabled():
    try:
        return bool(apps.get_app_config('djangocms_versioning'))
    except LookupError:
        return False
