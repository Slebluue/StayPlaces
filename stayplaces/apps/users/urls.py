from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^logout$', views.logout, name="logout"),
    url(r'^login$', views.login, name="login"),
    url(r'^trips$', views.trips, name="trips"),
    url(r'^trips/review/(?P<id>\d+)$', views.review, name="review"),
    url(r'^trips/review/host/(?P<id>\d+)$', views.host_review, name="host_review"),
    url(r'^trips/review/place/(?P<id>\d+)$', views.place_review, name="place_review"),
    url(r'^hosting$', views.hosting, name="host"),
    url(r'^hosting/(?P<id>\d+)$', views.listing, name="listing"),
    url(r'^users/show/(?P<id>\d+)$', views.profile, name="profile"),
    url(r'^users/edit$', views.edit_profile, name="edit_profile"),
    url(r'^users/edit/(?P<id>\d+)$', views.edit, name="edit"),
    url(r'^$', views.index, name="home"),
    url(r'^register$', views.register, name="register")
]
