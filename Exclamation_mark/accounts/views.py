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
    
class PostCategoryFilter(APIView):
    def get(self, request, format=None, category_number=None):
        #category_number = request.GET.get('category_number')
        posts = Post.objects.filter(category=category_number)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    
    
class AcceptRequest(APIView):
    def post(self, request, format=None):
        id = request.data.get('id')
        post = Post.objects.get(id=id)
        post.receiver = request.username
        post.save()
        return Response({'id': id})