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
    url(r'add_drug/$', views.add_drug, name='api_add_drug'),
    url(r'search_drug/$', views.search_drug, name='api_search_drug'),
    url(r'wish_drug/$', views.wishlist_drug, name='api_wishlist_drug'),
    url(r'stock_drug/$', views.stock_drug, name='api_stock_drug'),
    url(r'remove_drug/(?P<id>\d+)/$',
        views.remove_drug, name='api_remove_drug'),
    url(r'recent_drugs/(?P<count>\d+)/$',
        views.recent_drugs, name='api_recent_drugs'),
    url(r'request_drug/(?P<drug_id>\d+)/$',
        views.request_drug, name='api_request_drug'),
    url(r'pending/$', views.pending_requests, name='api_pending_requests'),
    url(r'accept/(?P<request_id>\d+)/$', views.accept, name='api_accept'),
    url(r'reject/(?P<request_id>\d+)/$', views.reject, name='api_reject'),
    url(r'drug_list/$', views.list_generic_drugs, name='api_drugs_list'),
]
