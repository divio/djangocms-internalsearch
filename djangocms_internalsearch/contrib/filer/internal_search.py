from django.utils.html import format_html
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


def get_absolute_url(obj):
    if obj.result.url:
        return format_html("<a href='{url}'>{url}</a>", url=obj.result.url)


get_absolute_url.short_description = _('URL')


class FilerFileConfig(BaseSearchConfig):
    # indexes definition
    folder_name = indexes.CharField(model_attr="folder__name")
    file_path = indexes.CharField(model_attr="file")
    title = indexes.CharField(model_attr="original_filename")
    file_size = indexes.IntegerField(model_attr="_file_size")
    created_by = indexes.CharField(model_attr="owner")
    version_status = indexes.CharField()
    url = indexes.CharField()

    # admin setting
    list_display = [get_title, get_absolute_url, get_file_size, get_file_path]
    search_fields = ('title', 'folder_name')
    list_filter = ()

    model = File

    def prepare_text(self, obj):
        # Todo: Might need to change based on file type e.g. Image
        return ' '.join([obj.original_filename, ])

    def prepare_url(self, obj):
        return obj.get_admin_change_url()


class FilerImageConfig(BaseSearchConfig):
    # indexes definition
    folder_name = indexes.CharField(model_attr="folder__name")
    file_path = indexes.CharField(model_attr="file")
    title = indexes.CharField(model_attr="original_filename")
    file_size = indexes.IntegerField(model_attr="_file_size")
    created_by = indexes.CharField(model_attr="owner")
    version_status = indexes.CharField()
    url = indexes.CharField()

    # admin setting
    list_display = [get_title, get_absolute_url, get_folder_name, get_file_size]
    search_fields = ('title', 'folder_name')
    list_filter = ()

    model = Image

    def prepare_text(self, obj):
        # Todo: Might need to change based on file type e.g. Image
        return ' '.join([obj.original_filename, ])

    def prepare_url(self, obj):
        return obj.get_admin_change_url()
