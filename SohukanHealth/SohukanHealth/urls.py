from SohukanHealth.views import home_page, demo
from api.v1.app_available_data import LineItemResource, read_data_resource
from django.conf.urls import patterns
from djangorestframework.views import ListOrCreateModelView
from monitor.views import learning_jquery, read, add

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', home_page),
                       (r'^demo/$', demo),
                       (r'^api/v1/demo', ListOrCreateModelView.as_view(resource=LineItemResource)),
                       (r'^monitor/learning_jquery/$', learning_jquery),
                       (r'^monitor/read/$', read),
                       (r'^monitor/add/$', add),
                       (r'^api/v1/monitor/read/$', ListOrCreateModelView.as_view(resource=read_data_resource)),
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
