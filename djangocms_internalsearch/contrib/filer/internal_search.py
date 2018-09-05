from filer.models.filemodels import File
from filer.models.imagemodels import Image
from haystack import indexes

from djangocms_internalsearch.base import BaseSearchConfig


class FilerFileConfig(BaseSearchConfig):
    # indexes definition
    folder_name = indexes.CharField(model_attr="folder__name")
    file_path = indexes.CharField(model_attr="file")
    title = indexes.CharField(model_attr="original_filename")
    file_size = indexes.IntegerField(model_attr="_file_size")
    created_by = indexes.CharField(model_attr="owner")
    version_status = indexes.CharField()

    # admin setting
    list_display = ['get_title', 'get_file_size', 'get_file_path']
    search_fields = ('title', 'folder_name')
    list_filter = ()

    model = File

    def get_title(self, obj):
        return obj.result.file_path
    get_title.short_description = 'Title'

    def get_file_path(self, obj):
        return obj.result.file_path
    get_file_path.short_description = 'File Path'

    def get_file_size(self, obj):
        return obj.result.file_size
    get_file_size.short_description = 'File Size'

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
    list_display = ['get_title', 'get_folder_name', 'get_file_size']
    search_fields = ('title', 'folder_name')
    list_filter = ()

    model = Image

    def get_title(self, obj):
        return obj.result.title
    get_title.short_description = 'Title'

    def get_folder_name(self, obj):
        return obj.result.folder_name
    get_folder_name.short_description = 'Folder Name'

    def get_file_size(self, obj):
        return obj.result.file_size
    get_file_size.short_description = 'File Size'

    def prepare_text(self, obj):
        # Todo: Might need to change based on file type e.g. Image
        return ' '.join([obj.original_filename, ])
