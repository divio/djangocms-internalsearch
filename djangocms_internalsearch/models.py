from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Query(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    query_time = models.DateTimeField(auto_now_add=True)
    query_string = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self):
        # TODO customise saving
        super().save()
