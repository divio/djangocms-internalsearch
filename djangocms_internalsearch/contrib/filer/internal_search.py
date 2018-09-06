from django.utils.translation import ugettext_lazy as _

from filer.models.filemodels import File
from filer.models.imagemodels import Image
from haystack import indexes

from djangocms_internalsearch.base import BaseSearchConfig


def get_title(obj):
    return obj.result.file_path


get_title.short_description = _('Title')


def get_file_path(obj):
    return obj.result.file_path


get_file_path.short_description = _('File Path')


def get_file_size(obj):
    return obj.result.file_size


get_file_size.short_description = _('File Size')


def get_folder_name(obj):
    return obj.result.folder_name


get_folder_name.short_description = _('Folder Name')


class FilerFileConfig(BaseSearchConfig):
    # indexes definition
    folder_name = indexes.CharField(model_attr="folder__name")
    file_path = indexes.CharField(model_attr="file")
    title = indexes.CharField(model_attr="original_filename")
    file_size = indexes.IntegerField(model_attr="_file_size")
    created_by = indexes.CharField(model_attr="owner")
    version_status = indexes.CharField()

    # admin setting
    list_display = [get_title, get_file_size, get_file_path]
    search_fields = ('title', 'folder_name')
    list_filter = ()

    model = File

    def prepare_text(self, obj):
        # Todo: Might need to change based on file type e.g. Image
        return ' '.join([obj.original_filename, ])


class FilerImageConfig(BaseSearchConfig):
    # indexes definition
    folder_name = indexes.CharField(model_attr="folder__name")
    file_path = indexes.CharField(model_attr="file")
    title = indexes.CharField(model_attr="original_filename")
    file_size = indexes.IntegerField(model_attr="_file_size")
    created_by = indexes.CharField(model_attr="owner")
    version_status = indexes.CharField()

    # admin setting
    list_display = [get_title, get_folder_name, get_file_size]
    search_fields = ('title', 'folder_name')
    list_filter = ()

    model = Image

    def prepare_text(self, obj):
        # Todo: Might need to change based on file type e.g. Image
        return ' '.join([obj.original_filename, ])
