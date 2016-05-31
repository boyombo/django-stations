from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'stations/$', views.get_stations, name='api_stations'),
    url(r'entry/(?P<station_id>\d+)/$', views.make_entry, name='api_entry'),
    url(r'new/$', views.add_station, name='api_add_station'),
    # Booking api
    url(r'booking/$', views.booking, name='api_booking'),
    # Insure api
    url(r'insure/$', views.insure, name='api_insure'),
    # Drugshare api
    url(r'register_pharm/$', views.register_pharm, name='api_register_pharm'),
]
