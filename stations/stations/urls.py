"""stations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from depot import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.station_list, name='show_list'),
    url(r'add/(?P<station_id>\d+)/$', views.add_entry, name='update'),
    url(r'station/$', views.add_station, name='add_station'),
    url(r'api/', include('api.urls'),),
    url(r'booking/', include('booking.urls'),),
    url(r'^accounts/login/$',
        login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Stations admin'
