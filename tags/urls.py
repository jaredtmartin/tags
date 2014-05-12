from django.conf.urls import patterns, include, url
from tags.views import (ListTags, EditTag, TagNameAjax, TagImageAjax, ShowTag, SearchTag, ReportTag, 
  RegisterTag, HowItWorks, Home)

#  For this project view and url names will follow verb_noun naming pattern.

urlpatterns = patterns('',
    url(r'^$', ListTags.as_view(), name='list_tags'),
    # url(r'^edit/(?P<object>\d+)/$', EditTag.as_view(), name='edit_tag'),
    url(r'^(?P<pk>\d+)/edit/$', EditTag.as_view(), name='edit_tag'),
    url(r'^(?P<pk>\d+)/$', ShowTag.as_view(), name='show_tag'),
    url(r'^(?P<pk>\d+)/name/$', TagNameAjax.as_view(), name='change_name'),
    url(r'^(?P<pk>\d+)/image/$', TagImageAjax.as_view(), name='change_image'),
    url(r'^(?P<pk>\d+)/report/$', ReportTag.as_view(), name="report"),
    url(r'^register/$', RegisterTag.as_view(), name="register"),
    url(r'^search/$', SearchTag.as_view(), name="search"),
    url(r'^howitworks/$', HowItWorks.as_view(), name="howitworks"),
   )