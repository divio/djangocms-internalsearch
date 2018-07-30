from haystack.indexes import (
    CharField,
    DateTimeField,
    Indexable,
    IntegerField,
    MultiValueField,
    SearchIndex,
)


class PageIndex(SearchIndex, Indexable):
    page_title = CharField(model_attr='cms_title')
    slug = CharField(model_attr='slug')
    site_id = IntegerField(model_attr='site_id')
    site_name = CharField(model_attr='site_name')
    language = CharField(model_attr='language')
    plugin_type_array = MultiValueField(model_attr='cms_plugin')
    text = CharField(document=True, use_template=False)
    created_by = CharField(model_attr='created_by')
    changed_by = CharField(model_attr='changed_by')
    version_status = CharField(model_attr='version_status')
    creation_date = DateTimeField(model_attr='creation_date')
    changed_date = DateTimeField(model_attr='changed_date')

    def prepare_page_title(self, obj):
        # TODO: prepare title (cms_title) field to save
        pass

    def prepare_slug(self, obj):
        # TODO: prepare slug/url (cms_title) to save
        pass

    def prepare_site_name(self, obj):
        # TODO: prepare sitename (cms_treenode) to save
        pass

    def prepare_plugin_type_array(self, obj):
        # TODO: preapare list of cms plugin (cms_plugin) used for specific page
        pass

    def prepare_text(self, obj):
        # TODO: perpare text as string to get rendered data of all cms plugin for
        # specific page
        pass
