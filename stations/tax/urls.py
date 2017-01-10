from django.conf.urls import url

from tax import views


urlpatterns = [
    url(r'^auth/', views.auth, name='tax_auth'),
    url(r'^search/', views.search, name='tax_search'),
]
