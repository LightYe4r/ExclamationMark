from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
]
