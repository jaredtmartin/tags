from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YesTags.views.home', name='home'),
    # url(r'^YesTags/', include('YesTags.foo.urls')),
		url(r'^admin/', include(admin.site.urls)),
    url(r'^tags/', include('tags.urls')),
)

## This is used to serve user uploaded files in dev mode
##if settings.DEBUG:
##    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)