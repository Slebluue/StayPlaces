from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="inbox"),
    url(r'^send/(?P<id>\d+)$', views.send, name="send"),
    url(r'^user-conversation/(?P<id>\d+)$', views.user_conversation, name="userconversation"),
    url(r'^host-conversation/(?P<id>\d+)$', views.host_conversation, name="hostconversation"),
]
