from django.conf.urls import patterns, include, url
from tags.views import (ListTags, EditTag, TagNameAjax, TagImageAjax, ShowTag, SearchTag, ReportTag, 
  RegisterTag, HowItWorks, Home, TagRewardAjax, DismissEvent, ViewEvent, ListClients, SMSFound, SMSRegister,
  DebugView, ListCodesView)

#  For this project view and url names will follow verb_noun naming pattern.

urlpatterns = patterns('',
    url(r'^$', ListTags.as_view(), name='list_tags'),
    # url(r'^edit/(?P<object>\d+)/$', EditTag.as_view(), name='edit_tag'),
    url(r'^(?P<pk>\d+)/edit/$', EditTag.as_view(), name='edit_tag'),
    url(r'^(?P<pk>\d+)/$', ShowTag.as_view(), name='show_tag'),
    url(r'^(?P<pk>\d+)/name/$', TagNameAjax.as_view(), name='change_name'),
    url(r'^(?P<pk>\d+)/reward/$', TagRewardAjax.as_view(), name='change_reward'),
    url(r'^(?P<pk>\d+)/image/$', TagImageAjax.as_view(), name='change_image'),
    url(r'^(?P<pk>\d+)/report/$', ReportTag.as_view(), name="report"),
    url(r'^register/$', RegisterTag.as_view(), name="registerAlt"),
    url(r'^search/$', SearchTag.as_view(), name="search"),
    url(r'^howitworks/$', HowItWorks.as_view(), name="howitworks"),
    url(r'^event/(?P<pk>\d+)/disregard/$', DismissEvent.as_view(), name="dismissEvent"),
    url(r'^event/(?P<pk>\d+)/$', ViewEvent.as_view(), name="viewEvent"),
    url(r'^clients/$', ListClients.as_view(), name="list_clients"),
    url(r'^sms/found/$',SMSFound.as_view(),name="SMS_found"),
    url(r'^sms/register/$',SMSRegister.as_view(),name="SMS_register"),
    url(r'^debug/', DebugView.as_view(), name='debug'),
    url(r'^codes/', ListCodesView.as_view(), name='list_codes'),
   )