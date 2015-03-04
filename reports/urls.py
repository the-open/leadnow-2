from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reports.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


    url(r'^$', 'reports.views.home', name='home'),

    url(r'^query/$', 'reports.views.query', name='query'),

    url(r'^importcsv/$', 'reports.views.import_csv', name='import_csv'),
)
