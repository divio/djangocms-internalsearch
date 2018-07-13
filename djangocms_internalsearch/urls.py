from django.conf.urls import url, include

from . import views

urlpatterns = [
        #url('', views.SearchView.as_view(), name='search'),
        url(r'^search/', include('haystack.urls')),
    ]
