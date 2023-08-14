from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Post
from.serializer import UserSerializer, PostSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class PostCategoryFilter(APIView):
    def get(self, request, format=None, category_name=None):
        posts = Post.objects.filter(category=category_name)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostUserFilter(APIView):
    def get(self, request, format=None, user_id=None):
        posts = Post.objects.filter(caller=user_id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostAccept(APIView):
    def get(self, request, format=None, post_id=None):
        posts = Post.objects.filter(receiver=None)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, post_id=None):
        post = Post.objects.get(id=post_id)
        post.receiver = request.user
        post.save()
        return Response({'result': 'success'})
    
class PostCreate(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        title = request.data['title']
        caller = request.user.username
        location_latitude = request.data['location_latitude']
        location_longitude = request.data['location_longitude']
        category = request.data['category']
        post = Post.objects.create(title=title, caller = caller, receiver = None, location_latitude=location_latitude, location_longitude=location_longitude, category=category)
        post.save()
        return Response({'result': 'success', 'created_at' : post.created_at})
    

    