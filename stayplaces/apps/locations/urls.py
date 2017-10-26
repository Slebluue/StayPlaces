from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^search$', views.search, name="search"),
    url(r'^rooms/(?P<id>\d+)$', views.show, name="show"),
    url(r'^rooms/(?P<id>\d+)/book$', views.book, name="book"),
]
