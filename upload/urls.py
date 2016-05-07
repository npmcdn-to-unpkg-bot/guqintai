#coding=utf8
from django.conf.urls import url
from upload import views as View
urlpatterns = [
    url('^$', View.Index.as_view()),
]
