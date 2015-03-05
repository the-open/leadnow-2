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
    url(r'^query/save/$', 'reports.views.query_save', name='query_save'),
    url(r'^query/(?P<query_id>\d+)/$', 'reports.views.query_details', name='query_details'),
    url(r'^report/$', 'reports.views.report', name='report'),
    url(r'^report/(?P<query_id>\d+)/$', 'reports.views.report', name='report'),

    url(r'^importcsv/$', 'reports.views.import_csv', name='import_csv'),
)
