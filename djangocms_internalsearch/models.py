from django.conf import settings
from django.db import models


class Query(models.Model):
    query_string = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class InternalSearchProxy(Query):
    class Meta:
        proxy = True
        verbose_name_plural = "Internal Search"
