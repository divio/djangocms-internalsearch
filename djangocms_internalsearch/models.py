from django.conf import settings
from django.db import models


class Query(models.Model):
    query_string = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Article(models.Model):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField()

    def __str__(self):
        return self.title
