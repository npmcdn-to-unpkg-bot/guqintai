#coding=utf8
from django.conf.urls import url
from blog import views as View
urlpatterns = [
    url('^$', View.Index.as_view()),
    url('^post', View.Post.as_view()),
]
