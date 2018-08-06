from django.conf import settings
from django.db import models


class Query(models.Model):
    query_string = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class AllIndex(models.Model):
    achar = models.TextField()
    adatetime = models.DateTimeField()
    aint = models.IntegerField()
    aurl = models.URLField()
    abool = models.BooleanField()
