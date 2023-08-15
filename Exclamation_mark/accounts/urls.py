from django.contrib import admin
from django.urls import path, include
from .views import UserViewSet, PostViewSet, MainHelper, MainAsker, Meeting, MeetingAfter, Recipient, Reqconfirm
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('users', UserViewSet)
routers.register('posts', PostViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('accounts/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('mainhelper/<str:category_name>/<int:post_id>/', MainHelper.as_view()),
    path('mainasker/<str:category_name>/<int:post_id>/', MainAsker.as_view()),
    path('meeting/<int:post_id>/<str:command>/', Meeting.as_view()),
    path('meetingafter/<int:post_id>/', MeetingAfter.as_view()),
    path('recipient/<str:category_name>/<str:latitude>/<str:longtitude>/<str:building_name>/<str:address>/', Recipient.as_view()),
    path('reqconfirm/<int:post_id>/', Reqconfirm.as_view()),
]
