from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from server.views import main_page, dcu_handler, ajax_handler

urlpatterns = patterns('',
	url(r'^$', main_page),
	url(r'^dcu/$', dcu_handler),
	url(r'^ajax/$', ajax_handler),
	url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
		        url(r'^static/(?P<path>.*)$', 'serve'),
						    )
