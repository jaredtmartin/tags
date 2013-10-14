from django.conf.urls import patterns, url
from tags.views import ListTags, EditTag, TagNameAjax, TagImageAjax

#  For this project view and url names will follow verb_noun naming pattern.

urlpatterns = patterns('',
    url(r'^$', ListTags.as_view(), name='list_tags'),
    # url(r'^edit/(?P<object>\d+)/$', EditTag.as_view(), name='edit_tag'),
    url(r'^(?P<pk>\d+)/$', EditTag.as_view(), name='show_tag'),
    url(r'^(?P<pk>\d+)/name/$', TagNameAjax.as_view(), name='change_name'),
    url(r'^(?P<pk>\d+)/image/$', TagImageAjax.as_view(), name='change_image'),
   )