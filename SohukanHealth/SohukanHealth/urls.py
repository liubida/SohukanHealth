from SohukanHealth.views import about, index, logtest, add_job_monitor, read_job_monitor, web_job_monitor
from django.conf.urls import patterns, include
from django.contrib import admin
from monitor.views import read, add, monitor, sys_alarm
from statistics.views import user_total, user_bookmark_percent, bookmark_total, \
    statistics, bookmark_per_user, bookmark_time, day_report, \
    day_report_bookmark_percent, day_report_bookmark_website, day_report_abstract, \
    day_report_date, depth, activate_user, week_report, bookmark_website, \
    user_platform, week_report_date, week_report_abstract, bookmark_website_detail, \
    week_report_bookmark_website, bookmark_website_for_user, share_channels, \
    bookmark_shorturl, bookmark_set_public, public_client, bookmark_email, \
    fiction_total, conversion

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', index),
                       (r'^monitor/?$', monitor),
                       (r'^monitor/sys_alarm/(?P<month>.*)/$', sys_alarm),
                       #(r'^monitor/sys_alarm/(?P<month>\d{4}-\d{2}-\d{2})/$', 'sys_alarm'),
                       (r'^monitor/read/?$', read),
                       (r'^monitor/read_job/?$', read_job_monitor),
                       (r'^monitor/add/?$', add),
                       (r'^monitor/add_job/?$', add_job_monitor),
                       (r'^monitor/web_job/?$', web_job_monitor),
                       (r'^statistics/user/total/?$', user_total),
                       (r'^statistics/user/bookmark_percent/?$', user_bookmark_percent),
                       (r'^statistics/bookmark/total/?$', bookmark_total),
                       (r'^statistics/bookmark/email/?$', bookmark_email),
                       (r'^statistics/fiction/total/?$', fiction_total),
                       (r'^statistics/bookmark/per_user/?$', bookmark_per_user),
                       (r'^statistics/bookmark/time/?$', bookmark_time),
                       (r'^statistics/bookmark/share_channels/?$', share_channels),
                       (r'^statistics/bookmark/public_client/?$', public_client),
                       (r'^statistics/bookmark/shorturl/?$', bookmark_shorturl),
                       (r'^statistics/bookmark/set-public/?$', bookmark_set_public),
                       (r'^statistics/?$', statistics),
                       (r'^statistics/depth/?$', depth),
                       (r'^statistics/depth/activate_user/?$', activate_user),
                       (r'^statistics/depth/conversion/?$', conversion),
                       (r'^statistics/depth/bookmark_website/?$', bookmark_website),
                       (r'^statistics/depth/bookmark_website_detail$/?', bookmark_website_detail),
                       (r'^statistics/depth/bookmark_website_for_user/?$', bookmark_website_for_user),
                       (r'^statistics/depth/platform/?$', user_platform),
                       (r'^statistics/day_report/?$', day_report),
                       (r'^statistics/day_report/date/?$', day_report_date),
                       (r'^statistics/day_report/abstract/?$', day_report_abstract),
                       (r'^statistics/day_report/bookmark_percent/?$', day_report_bookmark_percent),
                       (r'^statistics/day_report/bookmark_website/?$', day_report_bookmark_website),
                       (r'^statistics/week_report/?$', week_report),
                       (r'^statistics/week_report/date/?$', week_report_date),
                       (r'^statistics/week_report/abstract/?$', week_report_abstract),
                       (r'^statistics/week_report/bookmark_website/?$', week_report_bookmark_website),
                       (r'^about/?$', about),
                       (r'^logtest/?$', logtest),
                       (r'^admin/?', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.auth.views',
                        (r'^monitor/mlogin/?', 'login', {'template_name': 'login.html'}),
                        (r'^monitor/mlogout/?', 'logout', {'template_name': 'logout.html', 'next_page': '/'}),
)

#urlpatterns += patterns('django.contrib.auth.views', 
#                        (r'^internal/accounts/login/$', 'login', {'template_name': 'internal/auth/login.html'}),
#                        (r'^internal/accounts/logout/?$', 'logout', {'template_name': 'internal/auth/logout.html', 'next_page': '/internal/'}),
#)


