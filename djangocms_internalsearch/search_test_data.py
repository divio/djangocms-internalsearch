from django.utils import timezone

from .models import Article
import faker
fake = faker.Faker()


def create_search_test_data():
    for i in range(1, 10):
        a = Article()
        a.title = fake.name()
        a.slug = fake.name()
        a.description = fake.text()
        a.created_on = timezone.now()
        a.save()
