from django.conf.urls import url
from booking import views


urlpatterns = [
    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'reports/$', views.reports, name='reports'),
    url(r'register/$', views.register, name='register'),
    #url(r'showed_up/(?P<id>\+)$', views.showed_up, name='showed_up'),
    url(r'resident_list/$', views.resident_list, name='resident_list'),
    url(r'remove/(?P<id>\d+)/$', views.remove, name='remove_resident'),
]
