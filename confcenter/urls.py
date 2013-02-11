from django.conf.urls import patterns, include, url
from upload.views import upload_file, anal_acc, list_values, upload_progress, headpiece, dummy

from upload.models import Oses

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from confcenter import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'confcenter.views.home', name='home'),
    # url(r'^confcenter/', include('confcenter.foo.urls')),

    ('^$', headpiece),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/$', upload_file),
    url(r'^upload/$', upload_file),
    url(r'^projects/$', dummy),
    url(r'^plans/$', dummy),
    url(r'^about/$', dummy),
    url(r'^upload/progress/$', upload_progress, name='upload_progress'),
    url(r'^upload/anal_acc/$', anal_acc),
    url(r'^values/$', list_values),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^i18n/', include('django.conf.urls.i18n')),

)

if settings.DEBUG:
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )