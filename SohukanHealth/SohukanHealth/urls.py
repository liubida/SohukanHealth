from SohukanHealth.views import home_page
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', home_page),
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
