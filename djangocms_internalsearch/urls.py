from django.conf.urls import url

from . import views

urlpatterns = [
        url('', views.SearchView.as_view(), name='search'),
    ]
