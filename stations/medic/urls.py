from django.conf.urls import url

from medic import views


urlpatterns = [
    url(r'auth/$', views.authenticate, name='api_auth'),
    url(r'register/$', views.register, name='api_register'),
    url(r'initdata/$', views.initdata, name='api_initdata'),
    url(r'verify/$', views.verify, name='api_verify'),
    url(r'makerequest/$', views.makerequest, name='api_makerequest'),
    url(r'myrequests/$', views.myrequests, name='api_myrequests'),
    url(r'messages/(?P<id>\d+)/$', views.get_messages, name='api_messages'),
    url(r'addmessage/(?P<id>\d+)/$', views.add_message, name='api_addmessage'),
]
