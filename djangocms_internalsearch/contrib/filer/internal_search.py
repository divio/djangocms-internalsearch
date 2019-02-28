from django.apps import apps
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

import filer.settings
from haystack import indexes

from djangocms_internalsearch.base import BaseVersionableSearchConfig


def get_title(obj):
    return obj.result.file_path


get_title.short_description = _("Title")


def get_file_path(obj):
    return obj.result.file_path


get_file_path.short_description = _("File Path")


def get_file_size(obj):
    return obj.result.file_size


get_file_size.short_description = _("File Size")


def get_folder_name(obj):
    return obj.result.folder_name


get_folder_name.short_description = _("Folder Name")


def get_absolute_url(obj):
    if obj.result.url:
        return format_html("<a href='{url}'>{url}</a>", url=obj.result.url)


get_absolute_url.short_description = _("URL")


def get_version_status(obj):
    return obj.result.version_status


get_version_status.short_description = _("Version Status")


def get_version_author(obj):
    return obj.result.version_author


get_version_author.short_description = _("Author")


class BaseFilerConfig(BaseVersionableSearchConfig):
    # indexes definition
    folder_name = indexes.CharField(model_attr="folder__name")
    file_path = indexes.CharField(model_attr="file")
    title = indexes.CharField(model_attr="original_filename")
    file_size = indexes.IntegerField(model_attr="_file_size")
    url = indexes.CharField()

    # admin setting
    list_display = [
        get_title,
        get_absolute_url,
        get_version_status,
        get_version_author,
        get_file_size,
        get_file_path,
    ]
    search_fields = ("title", "folder_name")
    list_filter = ()

    model = None

    def prepare_text(self, obj):
        # Todo: Might need to change based on file type e.g. Image
        return " ".join(
            [obj.original_filename, obj.original_filename.rpartition(".")[0]]
        )

    def prepare_url(self, obj):
        return obj.get_admin_change_url()


def filer_model_config_factory():
    if not apps.is_installed("filer"):
        return []

    model_configs = []
    for model_name in filer.settings.FILER_FILE_MODELS:
        model_configs.append(
            type(
                model_name + "FilerConfig",
                (BaseFilerConfig,),
                {"model": apps.get_model(model_name)},
            )
        )
    return model_configs
