from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Post, Review
from.serializer import UserSerializer, PostSerializer, ReviewSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
# class PostCategoryFilter(APIView):
#     def get(self, request, format=None, category_name=None):
#         posts = Post.objects.filter(category=category_name)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
    
# class PostUserFilter(APIView):
#     def get(self, request, format=None, user_id=None):
#         posts = Post.objects.filter(caller=user_id)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
    
# class PostAccept(APIView):
#     def get(self, request, format=None, post_id=None):
#         posts = Post.objects.filter(receiver=None)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, post_id=None):
#         post = Post.objects.get(id=post_id)
#         post.receiver = request.user
#         post.save()
#         return Response({'result': 'success'})
    
# class PostCreate(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         title = request.data['title']
#         caller = request.user.username
#         location_latitude = request.data['location_latitude']
#         location_longitude = request.data['location_longitude']
#         category = request.data['category']
#         post = Post.objects.create(title=title, caller = caller, receiver = None, location_latitude=location_latitude, location_longitude=location_longitude, category=category)
#         post.save()
#         return Response({'result': 'success', 'created_at' : post.created_at})
    
class MainHelper(APIView):
    def get(self, request, format=None, category_name=None, post_id=None):
        if category_name == 'all':
            posts = Post.objects.filter(helper=None)
        else:
            posts = Post.objects.filter(category=category_name, helper=None)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None, category_name=None, post_id=None):
        if post_id != 'none':
            post = Post.objects.get(id=post_id)
            post.helper = request.user
            post.save()
            return Response({'result': 'success'})
    
class Meeting(APIView):
    def get(self, request, format=None, post_id=None, command=None):
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    def post(self, request, format=None, post_id=None, command=None):
        post = Post.objects.get(id=post_id)
        if command == 'cancel':
            post.delete()
            return Response({'result': 'delete success'})
        elif command == 'complete':
            post.isWorkDone = True
            post.save()
            return Response({'result': 'complete success'})
        elif command =='retry':
            post.helper = None
            post.save()
            return Response({'result': 'retry success'})
        else:
            return Response({'result': 'error'})
        
class MeetingAfter(APIView):
    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        if post.isWorkDone == True:
            review = Review.objects.get(post=post, asker = request.user)
            review_serializer = ReviewSerializer(review)
            return Response({'post': serializer.data, 'review': review_serializer.data})
        else:
            return Response({'result': 'not yet'})
    
    def post(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        if request.user.type == 'asker':
            review = Review.objects.create(post=post, asker = request.user, helper = post.helper ,score=request.data['score'], content=request.data['content'])
            review.save()
            return Response({'result': 'review success'})

    
class MainAsker(APIView):
    def get(self, request, format=None, category_name=None, post_id=None):
        if category_name == 'all':
            posts = Post.objects.all()
        else:
            posts = Post.objects.filter(category=category_name)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class Recipient(APIView):
    def get(self, request, format=None, category_name=None, latitude=None, longtitude=None, building_name=None, address=None, voice_record_name=None):
        return Response({'result': 'get Recipient success'})
    def post(self, request, format=None, category_name=None, latitude=None, longtitude=None, building_name=None, address=None, voice_record_name=None):
        post = Post.objects.create(category=category_name, location_latitude=float(latitude), location_longtitude=float(longtitude), 
                                   asker=request.user, helper=None, isWorkDone=False, building_name=building_name, address=address,
                                   voice_record_name=voice_record_name)
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)

class Reqconfirm(APIView):
    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)