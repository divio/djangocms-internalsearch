Integrating Internalsearch
==========================

.. toctree::
   :maxdepth: 1
   :caption: Contents:


Internalsearch is an optional feature, so the core CMS models and Third-party app's models
should be still usable when Internalsearch is not enabled.


Setting a config file
*****************************************************************

Any third-party app can use internalsearch functionality by adding 'cms_config.py`
with config class.

For example:

'myapp_name.cms_config.py'

.. code-block:: python

    from cms.app_base import CMSAppConfig

    class MyConfig(CMSAppConfig):
        djangocms_internalsearch_enabled = True
        intersearch_config_list = [<ModelConfigClass>, ]

`intersearch_config_list` is a list of model config class.


Let's say we have an app called 'publication' and the `Book` model that needs to integrate
in internal search.

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


To index `Book` model,  `publication` app should provide `cms_config.py`.

Config class can inherit one of two base config class from `djangocms_internalsearch.base.py`.
There are two base config classes provided by Internalsearch, `BaseSearchConfig` and `BaseVersionableSearchConfig`.
**BaseSearchConfig** should be base class of config for a non-versionable model, While
**BaseVersionableSearchConfig** should be base class of config for a versionable model. These
base config classes provide default attributes and configuration.



Configuration class consist of two-part of configuration. Index configuration for internal search
and Django admin configuration to display this information on django admin UI.
Read more on index configuration at `haystack documentation <https://django-haystack.readthedocs.io/en/master/searchindex_api.html>`_

Here is config class for `Book` model:

`publication.cms_config.py`

.. code-block:: python

    from djangocms_internalsearch.base import BaseSearchConfig

    from publication.models import Book

    class BookConfig(BaseSearchConfig):

        # admin configuration
        list_display = [
            get_name,
            get_pages,
            get_price,
            get_rating,
            get_rating,
            get_authors,
            get_pubdate,
        ]

        def get_name(self, obj):
            return getattr(obj, 'name')

        def get_pages(self, obj):
            return getattr(obj, 'pages')

        def get_price(self, obj):
            return getattr(obj, 'price')

        def get_rating(self, obj):
            return getattr(obj, 'rating')

        def get_author(self, obj):
            return getattr(obj, 'author')

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

