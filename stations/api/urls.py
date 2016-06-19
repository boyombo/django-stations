from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'stations/$', views.get_stations, name='api_stations'),
    url(r'entry/(?P<station_id>\d+)/$', views.make_entry, name='api_entry'),
    url(r'new/$', views.add_station, name='api_add_station'),
    # Booking api
    url(r'booking/(?P<resident_id>\d+)/$', views.booking, name='api_booking'),
    url(r'book_profile/$', views.book_profile, name='api_book_profile'),
    url(r'book_phone/$', views.book_phone, name='api_book_phone'),
    url(r'book_code/$', views.book_code, name='api_book_code'),
    # Insure api
    url(r'insure/$', views.insure, name='api_insure'),
    # Drugshare api
    url(r'register_pharm/$', views.register_pharm, name='api_register_pharm'),
    url(r'make_token/(?P<device_id>\d+)/$',
        views.make_token, name='api_make_token'),
    url(r'add_device/$', views.add_device, name='api_add_device'),
    url(r'get_profile/$', views.get_profile, name='api_get_profile'),
    url(r'update_pharm/(?P<device_id>\d+)/$',
        views.update_pharm, name='api_update_pharm'),
    url(r'add_outlet/(?P<device_id>\d+)/$',
        views.add_outlet, name='api_add_outlet'),
    url(r'delete_outlet/(?P<id>\d+)/$',
        views.delete_outlet, name='api_delete_outlet'),
    url(r'add_drug/$', views.add_drug, name='api_add_drug'),
    url(r'edit_drug/(?P<id>\d+)/$', views.edit_drug, name='api_edit_drug'),
    url(r'search_drug/(?P<device_id>\d+)/$',
        views.search_drug, name='api_search_drug'),
    url(r'wish_drug/(?P<device_id>\d+)/$',
        views.wishlist_drug, name='api_wishlist_drug'),
    url(r'stock_drug/(?P<device_id>\d+)/$',
        views.stock_drug, name='api_stock_drug'),
    url(r'remove_drug/(?P<id>\d+)/$',
        views.remove_drug, name='api_remove_drug'),
    url(r'recent_drugs/(?P<count>\d+)/$',
        views.recent_drugs, name='api_recent_drugs'),
    url(r'request_drug/(?P<drug_id>\d+)/$',
        views.request_drug, name='api_request_drug'),
    url(r'pending/(?P<device_id>\d+)/$',
        views.pending_requests, name='api_pending_requests'),
    url(r'accept/(?P<request_id>\d+)/$', views.accept, name='api_accept'),
    url(r'reject/(?P<request_id>\d+)/$', views.reject, name='api_reject'),
    url(r'drug_list/$', views.list_generic_drugs, name='api_drugs_list'),
    url(r'feedback/(?P<id>\d+)/$', views.feedback, name='api_feedback'),
]
