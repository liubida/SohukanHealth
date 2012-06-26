from SohukanHealth.views import home_page, demo, about, all
from api.v1.app_available_data import LineItemResource, read_data_resource
from django.conf.urls import patterns
from djangorestframework.views import ListOrCreateModelView
from monitor.views import read, add, monitor
from statistics.views import user_total, bookmark_total, statistics, \
    bookmark_per_user, bookmark_time

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', all),
                       (r'^demo/$', demo),
                       (r'^api/v1/demo', ListOrCreateModelView.as_view(resource=LineItemResource)),
                       (r'^monitor/$', monitor),
                       (r'^monitor/read/$', read),
                       (r'^monitor/add/$', add),
                       (r'^statistics/user/total$', user_total),
                       (r'^statistics/bookmark/total$', bookmark_total),
                       (r'^statistics/bookmark/per_user$', bookmark_per_user),
                       (r'^statistics/bookmark/time$', bookmark_time),
                       (r'^statistics/$', statistics),
                       (r'^all/$', all),
                       (r'^about/$', about),
#                       (r'^now/$', now),
#                       (r'^now/plus/(\d{1,2})/$', now_plus),
#                       (r'^hello/$', hello),
#                       (r'^dbo/$', dbo_page),
                        
    # Examples:
    # url(r'^$', 'SohukanHealth.views.home', name='home'),
    # url(r'^SohukanHealth/', include('SohukanHealth.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
