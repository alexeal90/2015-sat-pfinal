from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'final.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^login$', 'webapp.views.auth_view'),
	#url(r'^logout$', 'webapp.views.logout'),
	url(r'^actividad/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_URL2}),
	url(r'^actividad/(\d+)$', 'webapp.views.actividad'),
	url(r'^todas$', 'webapp.views.ordenar'),
	url(r'^ayuda$', 'webapp.views.ayuda'),
	url(r'^add', 'webapp.views.addEve'),
	url(r'^modcss$', 'webapp.views.modCSS'),
	url(r'^actualizar$', 'webapp.views.refresh'),
	url(r'^$', 'webapp.views.init'),
	url(r'^css/(?P<path>.*)$','django.views.static.serve', {'document_root' : settings.STATIC_URL2}),
	url(r'^(.*)/rss', 'webapp.views.rss'),
	url(r'^(.*)', 'webapp.views.user'),
)
