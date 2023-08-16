from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Post, Review
from.serializer import UserSerializer, PostSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class Login(APIView):
    def post(self, request, *args, **kwargs):
        # TODO: check if user exists & password is correct
        user = User.objects.get(username=request.data['username'])
        token = TokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        })
        
# TODO: implement
class Register(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.create(username=request.data['username'], password=request.data['password'])
        user.save()
        return Response({'result': 'success'})
    
class MainHelper(APIView):
    def get(self, request, format=None):
        posts = Post.objects.filter(helper=None)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        post_id = request.data['post_id']
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
        # if post.isWorkDone == True:
        #     review = Review.objects.get(post=post, asker = request.user)
        #     review_serializer = ReviewSerializer(review)
        #     return Response({'post': serializer.data, 'review': review_serializer.data})
        # else:
        #     return Response({'result': 'not yet'})
        return Response(serializer.data)
    
    def post(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        if post.asker == request.user:
            review = Review.objects.create(post=post, asker = request.user, helper = post.helper ,score=request.data['score'], content=request.data['content'])
            review.save()
            helper = User.objects.get(id=post.helper.id)
            helper.task_count += 1
            helper.score = (helper.score * (helper.task_count - 1) + float(request.data['score'])) / helper.task_count
            if request.data['content'] == 'kind':
                helper.kind_count += 1
            elif request.data['content'] == 'easy':
                helper.easy_count += 1
            elif request.data['content'] == 'endure':
                helper.endure_count += 1
            elif request.data['content'] == 'fast':
                helper.fast_count += 1
            elif request.data['content'] == 'etc':
                helper.etc_count += 1
            helper.save()
            return Response({'result': 'review success'})

    
# class MainAsker(APIView):
#     def get(self, request, format=None, category_name=None):
#         if category_name == 'all':
#             posts = Post.objects.all()
#         else:
#             posts = Post.objects.filter(category=category_name)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
class MainAsker(APIView):
    def get(self, request, format=None):
        category_name = request.data['category_name']
        if category_name == 'all':
            posts = Post.objects.all()
        else:
            posts = Post.objects.filter(category=category_name)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# class Recipient(APIView):
#     def get(self, request, format=None, category_name=None, latitude=None, longtitude=None, building_name=None, address=None, voice_record_name=None):
#         return Response({'result': 'get Recipient success'})
#     def post(self, request, format=None, category_name=None, latitude=None, longtitude=None, building_name=None, address=None, voice_record_name=None):
#         post = Post.objects.create(category=category_name, location_latitude=float(latitude), location_longtitude=float(longtitude), 
#                                    asker=request.user, helper=None, isWorkDone=False, building_name=building_name, address=address,
#                                    voice_record_name=voice_record_name)
#         post.save()
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
class Recipient(APIView):
    def get(self, request, format=None):
        return Response({'result': 'get Recipient success'})
    def post(self, request, format=None):
        category_name = request.data['category_name']
        latitude = request.data['latitude']
        longtitude = request.data['longtitude']
        building_name = request.data['building_name']
        address = request.data['address']
        voice_record_name = request.data['voice_record_name']
        asker = User.objects.get(id=1)
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