from django.contrib import admin
from django.urls import path, include
from .views import UserViewSet, PostViewSet, MainHelper, MainAsker, Meeting, MeetingAfter, Recipient, Reqconfirm, Login, Register, SelectHelper
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('users', UserViewSet)
routers.register('posts', PostViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('accounts/login/', Login.as_view()),
    path('registration/', Register.as_view()),
    path('mainhelper/', MainHelper.as_view()),
    path('mainasker/', MainAsker.as_view()),
    path('selecthelper/<int:post_id>/', SelectHelper.as_view()),
    path('meeting/<int:post_id>/', Meeting.as_view()),
    path('meetingafter/<int:post_id>/', MeetingAfter.as_view()),
    path('recipient/', Recipient.as_view()),
    path('reqconfirm/<int:post_id>/', Reqconfirm.as_view()),
]
