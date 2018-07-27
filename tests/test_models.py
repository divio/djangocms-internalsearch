from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from djangocms_internalsearch.models import Query


class QueryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', first_name='name')

    def test_query_save(self):
        query = Query()
        query.content_type = ContentType.objects.get_for_model(User)
        query.query_string = "?fbool__exact=1&q=bob"  # made up query string
        query.user = self.user
        query.save()

        user_queries = Query.objects.filter(user=self.user)
        # For now we expect what we put in is what we get out
        self.assertEqual(query, user_queries[0])
