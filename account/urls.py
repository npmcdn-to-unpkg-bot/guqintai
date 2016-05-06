#coding=utf8
from django.conf.urls import url
from account import views as View
urlpatterns = [
    url('^login$', View.Login.as_view()),
    url('^logout$', View.Logout.as_view()),
]
