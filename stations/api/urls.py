from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'stations/$', views.get_stations, name='api_stations'),
]
