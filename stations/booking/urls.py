from django.conf.urls import url
from booking import views


urlpatterns = [
    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'remove/(?P<id>\d+)/$', views.remove, name='remove_resident'),
]
