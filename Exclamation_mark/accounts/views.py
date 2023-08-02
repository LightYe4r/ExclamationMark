from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Post
from.serializer import UserSerializer, PostSerializer, RequestSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class RequestViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = RequestSerializer
    
class AcceptRequest(APIView):
    def post(self, request, format=None):
        post_id = request.data.get('post_id')
        post = Post.objects.get(post_id=post_id)
        post.receiver = request.username
        post.save()
        return Response({'post_id': post_id})