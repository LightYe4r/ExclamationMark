from django.contrib import admin
from django.urls import path, include
from .views import UserViewSet, PostViewSet, RequestViewSet, AcceptRequest, PostCategoryFilter
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('users', UserViewSet)
routers.register('posts', PostViewSet)
routers.register('requests', RequestViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('accounts/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('Accept/<int:pk>/', AcceptRequest.as_view()),
    path('posts/category/<int:category_number>', PostCategoryFilter.as_view()),
]
