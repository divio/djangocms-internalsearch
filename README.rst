*************************
django CMS Internalsearch
*************************

============
Installation
============

Requirements
============

django CMS Internalsearch requires that you have a django CMS 4.0 (or higher) project already running and set up.

This package also expects to connect to an Elasticsearch server using `django-haystack`. The use of Haystack in this project only support elasticsearch 2.X backend. You can find versions for all operating systems at: https://www.elastic.co/downloads/past-releases


To install
==========

Run::

    pip install git+git://github.com/divio/djangocms-internalsearch@master#egg=djangocms-internalsearch

Add the following to your project's ``INSTALLED_APPS``:

  - ``'djangocms_internalsearch'``

Add following line in project level urls.py after 'url(r'^admin/', include(admin.site.urls)),'

- ``url(r'^djangocms_internalsearch/', include('djangocms_internalsearch.urls')),``

Run::

    python manage.py migrate djangocms_internalsearch

to perform the application's database migrations.


Project configuration
---------------------

Within your `settings.py`, you’ll need to add a setting to indicate which backend to use, as well as other settings for that backend including URL for
elasticsearch and index name.

HAYSTACK_CONNECTIONS is a required setting and an example configuration is provided below:

`settings.py`

.. code-block:: python

    HAYSTACK_CONNECTIONS = {
       'default': {
           'ENGINE': 'djangocms_internalsearch.backends.elasticsearch2.InternalSearchESEngine',
           'URL': 'http://127.0.0.1:9200/',
           'INDEX_NAME': 'haystack',
       },
    }

To rebuild indexes manually
===========================

```./manage.py rebuild_index```
```./manage.py help```
and you will see all the options under haystack
or it should fire every time you create a page via signals
try do a `./manage.py clear_index` before ./reload_db.sh
that should also trigger

Documentation
=============

We maintain documentation under ``docs`` folder using rst format. HTML documentation can be generated using the following command

Run::

    cd docs/
    make html

This should generate all html files from rst documents under the `docs/_build` folder, which can be browsed.
