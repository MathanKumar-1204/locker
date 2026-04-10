from django.contrib import admin
from django.urls import path, include
from accounts.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/auth/', include('accounts.urls')),
    path('api/lockers/', include('lockers.urls')),
    path('api/reservations/', include('reservations.urls')),
]