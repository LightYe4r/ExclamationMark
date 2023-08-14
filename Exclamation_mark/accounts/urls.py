from django.contrib import admin
from django.urls import path, include
from .views import UserViewSet, PostViewSet, PostCategoryFilter, PostUserFilter, PostAccept, PostCreate
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('users', UserViewSet)
routers.register('posts', PostViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('accounts/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('posts/category/<str:category_name>', PostCategoryFilter.as_view()),
    path('posts/user/<int:user_id>', PostUserFilter.as_view()),
    path('posts/accept/<int:post_id>', PostAccept.as_view()),
    path('posts/create/', PostCreate.as_view()),
]
