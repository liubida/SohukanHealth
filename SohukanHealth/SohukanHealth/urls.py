from SohukanHealth.views import about, index, logtest
from api.v1.app_available_data import LineItemResource
from django.conf.urls import patterns
from djangorestframework.views import ListOrCreateModelView
from monitor.views import read, add, monitor, sys_alarm
from statistics.views import user_total, user_bookmark_percent, bookmark_total, \
    statistics, bookmark_per_user, bookmark_time, day_report, \
    day_report_bookmark_percent, day_report_bookmark_website, day_report_abstract, \
    day_report_date, depth, activate_user, week_report, bookmark_website, \
    user_platform

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', index),
                       (r'^api/v1/demo', ListOrCreateModelView.as_view(resource=LineItemResource)),
                       (r'^monitor/$', monitor),
                       (r'^monitor/sys_alarm/(?P<month>\d+)/$', sys_alarm),
                       (r'^monitor/read/$', read),
                       (r'^monitor/add/$', add),
                       (r'^statistics/user/total$', user_total),
                       (r'^statistics/user/bookmark_percent$', user_bookmark_percent),
                       (r'^statistics/bookmark/total$', bookmark_total),
                       (r'^statistics/bookmark/per_user$', bookmark_per_user),
                       (r'^statistics/bookmark/time$', bookmark_time),
                       (r'^statistics/$', statistics),
                       (r'^statistics/depth$', depth),
                       (r'^statistics/depth/activate_user$', activate_user),
                       (r'^statistics/depth/bookmark_website$', bookmark_website),
                       (r'^statistics/depth/platform$', user_platform),
                       (r'^statistics/day_report$', day_report),
                       (r'^statistics/day_report/date', day_report_date),
                       (r'^statistics/day_report/abstract$', day_report_abstract),
                       (r'^statistics/day_report/bookmark_percent$', day_report_bookmark_percent),
                       (r'^statistics/day_report/bookmark_website$', day_report_bookmark_website),
                       (r'^statistics/week_report$', week_report),
                       (r'^all/$', index),
                       (r'^about/$', about),
                       (r'^logtest/$', logtest),
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
