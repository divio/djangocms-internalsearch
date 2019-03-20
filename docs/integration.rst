Integrating Internalsearch
==========================

.. toctree::
   :maxdepth: 1
   :caption: Contents:


Internalsearch is an optional feature, so the core CMS models and third-party app models
should still be usable when Internalsearch is not enabled.


Setting a config file
*****************************************************************

Any third-party app can use internalsearch functionality by adding 'cms_config.py`
with a config class.

For example:

'myapp_name.cms_config.py'

.. code-block:: python

    from cms.app_base import CMSAppConfig

    class MyConfig(CMSAppConfig):
        djangocms_internalsearch_enabled = True
        intersearch_config_list = [<ModelConfigClass>, ]

`intersearch_config_list` is a list of model config class.


Let's say we have an app called 'publication' and the a `Book` model that needs to integrate
with internal search.

`publication.models.py`

.. code-block:: python

    class Author(models.Model):
        name = models.CharField(max_length=100)
        age = models.IntegerField()


    class Book(models.Model):
        name = models.CharField(max_length=300)
        pages = models.IntegerField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        rating = models.FloatField()
        author = models.ForeignKey(Author, on_delete=models.CASCADE)
        pubdate = models.DateField()


To index the `Book` model,  `publication` app should provide `cms_config.py` with model configuration.

Config class can inherit from one of two base config class provided by at `djangocms_internalsearch.base.py`.
`BaseSearchConfig` and `BaseVersionableSearchConfig`.

A Model can be made versionable by installing 'djangocms_versioning' app and provide configuration for a particular model.
Internalsearch provide base configurations to caters versionable and non-versoinable model to index.

**BaseSearchConfig** should be the base class of a config for a non-versionable model, While
**BaseVersionableSearchConfig** should be the base class of a config for a versionable model. These
base config classes provide default attributes and configuration.


You will need to configure the haystack indexes (internal search uses django-haystack under the hood) and the django admin UI through settings in the config class.
Read more on index configuration at `haystack documentation <https://django-haystack.readthedocs.io/en/master/searchindex_api.html>`_

Here is config class for `Book` model:

`publication.cms_config.py`

.. code-block:: python

    from djangocms_internalsearch.base import BaseSearchConfig

    from publication.models import Book

    class BookConfig(BaseSearchConfig):

        # admin configuration
        list_display = [
            "name",
            "pages",
            "price",
            "rating",
            "author",
            "pubdate",
        ]

        # Index configuration
        name = indexes.CharField(model_attr="name")
        pages = indexes.CharField(model_attr="pages")
        price = indexes.CharField(model_attr="price")
        rating = indexes.CharField(model_attr="rating")
        author = indexes.CharField(model_attr="author")
        pubdate = indexes.DateTimeField(model_attr="pubdate")

        # Additional foreign field for index
        author = indexes.CharField()

        model = Book
        list_per_page = 50

        def prepare_author(self, obj):
            # Do the computation and return the string
            # to save into index as author
            author = Author.objects.get(id=getatts(obj, 'author'))
            return author.name


    class InternalSearchConfig(CMSAppConfig):
        djangocms_internalsearch_enabled = True
        intersearch_config_list = [BookConfig, ]
