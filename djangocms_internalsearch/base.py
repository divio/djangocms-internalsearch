from django.contrib.admin.utils import unquote
from django.db.models import Max
from django.db.models.expressions import OuterRef, Subquery

from haystack import indexes

from djangocms_internalsearch.helpers import (
    get_version_object,
    get_versioning_extension,
)


class BaseSearchConfig(indexes.SearchIndex, indexes.Indexable):
    """
    Base config class to provide list of attributes that sub class must provide
    """
    text = indexes.CharField(document=True, use_template=False)
    text_ngram = indexes.NgramField(document=False, use_template=False)

    # admin setting
    list_per_page = 50

    @property
    def model(self):
        raise NotImplementedError("Config class must provide model attribute")

    @property
    def list_display(self):
        raise NotImplementedError("Config class must provide list_display fields")

    def get_model(self):
        return self.model

    def prepare_text(self, obj):
        raise NotImplementedError("Config class must provide prepare_text method for index")

    def prepare_text_ngram(self, obj):
        return self.prepare_text(obj)


class BaseVersionableSearchConfig(BaseSearchConfig):
    version_author = indexes.CharField()
    version_status = indexes.CharField()
    is_latest_version = indexes.BooleanField()

    def prepare_version_status(self, obj):
        version_obj = get_version_object(obj)
        if not version_obj:
            return
        return version_obj.state

    def prepare_version_author(self, obj):
        version_obj = get_version_object(obj)
        if not version_obj:
            return
        return version_obj.created_by.username

    def prepare_is_latest_version(self, obj):
        latest_pk = getattr(obj, 'latest_pk', None)
        return obj.pk == latest_pk

    def annotated_model_queryset(self, using=None):
        """Returns a model queryset annotated with latest_pk,
        the primary key corresponding to the latest version
        """
        versioning_extension = get_versioning_extension()
        versionable = versioning_extension.versionables_by_content.get(self.model)
        fields = {
            field: OuterRef(field)
            for field in versionable.grouping_fields
        }
        inner = self.model._base_manager.filter(
            **fields
        ).annotate(
            version=Max('versions__number')
        ).order_by('-version').values('pk')
        return self.model._base_manager.using(using).annotate(latest_pk=Subquery(inner[:1]))

    def index_queryset(self, using=None):
        versioning_extension = get_versioning_extension()
        if versioning_extension and versioning_extension.is_content_model_versioned(self.model):
            return self.annotated_model_queryset()
        else:
            return super().index_queryset(using)
