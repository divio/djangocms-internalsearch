from django.contrib.auth.models import User
from django.db import models


class Query(models.Model):
    query_time = models.DateTimeField(auto_now_add=True)
    query_string = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # TODO validate/clean before saving
        super().save(*args, **kwargs)
