from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Query(models.Model):
    query_string = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class InternalSearchProxy(Query):
    class Meta:
        permissions = []
        proxy = True
        verbose_name = _("Internal Search")
        verbose_name_plural = _("Internal Search")
