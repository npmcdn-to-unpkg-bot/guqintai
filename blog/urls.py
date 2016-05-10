#coding=utf8
from django.conf.urls import url
from blog import views as View
urlpatterns = [
    url('^$', View.Index.as_view()),
    url('^post', View.Post.as_view()),
    url('^edit/(?P<id>\w+)/$', View.Edit.as_view()),


    url('^list/', View.List.as_view()),
    url('^article/(?P<id>\w+)/', View.Detail.as_view()),
    url('^archive/(?P<id>\d+)/$', View.Archive.as_view()),


]
