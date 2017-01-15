from django.conf.urls import url

from parcel import views


urlpatterns = [
    url(r'register/$', views.register, name='parcel_register'),
    url(r'load/$', views.load, name='parcel_load'),
    url(r'arrival/$', views.arrival, name='parcel_arrival'),
    url(r'arrived/$', views.arrived_parcels, name='parcel_arrived'),
    url(r'pickup/(?P<id>\d+)/$', views.pickup, name='parcel_pickup'),
    url(r'status/$', views.status, name='parcel_status'),
]
