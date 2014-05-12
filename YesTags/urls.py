from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy
from tags.views import Home
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YesTags.views.home', name='home'),
    # url(r'^YesTags/', include('YesTags.foo.urls')),
    url(r'^$', Home.as_view(), name='home'),
		url(r'^admin/', include(admin.site.urls)),
    url(r'^tags/', include('tags.urls')),
    url(r'^auth/', include('authentication.urls')),
    # url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),

)

# This is used to serve user uploaded files in dev mode
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)