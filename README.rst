*************************
django CMS Internalsearch
*************************

============
Installation
============

Prerequisetes
============
This package expects to connect to an Elasticsearch server. For development, the use of Haystack in this project requirements are currently elsticsearch 2.X
You can find versions for all operating systems at: https://www.elastic.co/downloads/past-releases


Requirements
============

django CMS Internalsearch requires that you have a django CMS 3.5.0 (or higher) project already running and set up.


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


To rebuild indexes manually
===========================

```./manage.py rebuild_index```
```./manage.py help```
and you will see all the options under haystack
or it should fire every time you create a page via signals
try do a `./manage.py clear_index` before ./reload_db.sh
that should also trigger
