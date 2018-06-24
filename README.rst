*********************
django CMS Internalsearch
*********************

============
Installation
============

Requirements
============

django CMS Internalsearch requires that you have a django CMS 3.4.3 (or higher) project already running and set up.


To install
==========

Run::

    pip install git+git://github.com/divio/djangocms-internalsearch@develop#egg=djangocms-internalsearch

Add the following to your project's ``INSTALLED_APPS``:

  - ``'djangocms_internalsearch'``

Add following line in project level urls.py after 'url(r'^admin/', include(admin.site.urls)),'

- ``url(r'^djangocms_internalsearch/', include('djangocms_internalsearch.urls')),``

Run::

    python manage.py migrate djangocms_internalsearch

to perform the application's database migrations.
