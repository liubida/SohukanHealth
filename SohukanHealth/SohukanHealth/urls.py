from SohukanHealth.views import about, index, logtest
from api.v1.app_available_data import LineItemResource
from django.conf.urls import patterns, include
from django.contrib import admin
from djangorestframework.views import ListOrCreateModelView
from monitor.views import read, add, monitor, sys_alarm
from statistics.views import user_total, user_bookmark_percent, bookmark_total, \
    statistics, bookmark_per_user, bookmark_time, day_report, \
    day_report_bookmark_percent, day_report_bookmark_website, day_report_abstract, \
    day_report_date, depth, activate_user, week_report, bookmark_website, \
    user_platform, week_report_date, week_report_abstract, bookmark_website_detail, \
    week_report_bookmark_website, bookmark_website_for_user, share_channels

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

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
                       (r'^statistics/bookmark/share_channels$', share_channels),
                       (r'^statistics/$', statistics),
                       (r'^statistics/depth$', depth),
                       (r'^statistics/depth/activate_user$', activate_user),
                       (r'^statistics/depth/bookmark_website$', bookmark_website),
                       (r'^statistics/depth/bookmark_website_detail$', bookmark_website_detail),
                       (r'^statistics/depth/bookmark_website_for_user$', bookmark_website_for_user),
                       (r'^statistics/depth/platform$', user_platform),
                       (r'^statistics/day_report$', day_report),
                       (r'^statistics/day_report/date', day_report_date),
                       (r'^statistics/day_report/abstract$', day_report_abstract),
                       (r'^statistics/day_report/bookmark_percent$', day_report_bookmark_percent),
                       (r'^statistics/day_report/bookmark_website$', day_report_bookmark_website),
                       (r'^statistics/week_report$', week_report),
                       (r'^statistics/week_report/date/$', week_report_date),
                       (r'^statistics/week_report/abstract$', week_report_abstract),
                       (r'^statistics/week_report/bookmark_website/$', week_report_bookmark_website),
                       (r'^about/$', about),
                       (r'^logtest/$', logtest),
                       (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.auth.views',
                        (r'^monitor/mlogin', 'login', {'template_name': 'login.html'}),
                        (r'^monitor/mlogout', 'logout', {'template_name': 'logout.html', 'next_page': '/'}),
)

#urlpatterns += patterns('django.contrib.auth.views', 
#                        (r'^internal/accounts/login/$', 'login', {'template_name': 'internal/auth/login.html'}),
#                        (r'^internal/accounts/logout/?$', 'logout', {'template_name': 'internal/auth/logout.html', 'next_page': '/internal/'}),
#)


