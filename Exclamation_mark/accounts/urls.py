from django.contrib import admin
from django.urls import path, include
from .views import UserViewSet, PostViewSet, MainHelper, MainAsker, Meeting, MeetingAfter, Recipient, Reqconfirm, Login
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('users', UserViewSet)
routers.register('posts', PostViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('accounts/login/', Login.as_view()),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('mainhelper/', MainHelper.as_view()),
    path('mainasker/', MainAsker.as_view()),
    path('meeting/<int:post_id>/<str:command>/', Meeting.as_view()),
    path('meetingafter/<int:post_id>/', MeetingAfter.as_view()),
    path('recipient/', Recipient.as_view()),
    path('reqconfirm/<int:post_id>/', Reqconfirm.as_view()),
]
