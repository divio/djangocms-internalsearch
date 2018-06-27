from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class InternalSearch(models.Model):
    query = models.CharField(
        default='',
        blank=False,
        max_length=255
        )

    def __str__(self):
            return self.query

    class Meta:
        verbose_name = _('Search')
        verbose_name_plural = _("Searches")
        db_table = "djangocms_internalsearch"
