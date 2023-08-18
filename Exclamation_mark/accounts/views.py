from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User, Post, Review
from.serializer import UserSerializer, PostSerializer, ReviewSerializer, AskerSerializer, HelperSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import datetime
from django.db import IntegrityError

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
class Login(APIView):
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is None:
            return Response({'result': 'login fail'})
        else:
            token = TokenObtainPairSerializer.get_token(user)
            return Response({
                'refresh_token': str(token),
                'access_token': str(token.access_token),
                'type' : user.type
            })
        
# TODO: implement
class Register(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.create( username=request.data['username'],
                                    nickname=request.data['nickname'], 
                                    type=request.data['type'], 
                                    gender = request.data['gender'],
                                    birth_Year=request.data['birth_Year'],  
                                    birth_Month=request.data['birth_Month'],
                                    birth_Day=request.data['birth_Day'],
                                    )
            user.age = datetime.datetime.now().year - int(user.birth_Year) + 1
            user.age_range = user.age // 10 * 10
            user.set_password(request.data['password'])
            user.save()
            return Response({'result': 'success'})
        except IntegrityError as e:
            return Response({"ERROR": str(e)})
    
class MainHelper(APIView):
    def get(self, request, format=None):
        posts = Post.objects.filter(helper=None)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class SelectHelper(APIView):
    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=post.asker.id)
        serializer = AskerSerializer({"post": post, "asker": user})
        return Response(serializer.data)
    
    def post(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        post.helper = request.user
        user = User.objects.get(id=request.user.id)
        user.user_latitude = request.data['latitude']
        user.user_longtitude = request.data['longtitude']
        post.save()
        user.save()
        return Response({'result': 'success'})
    
class Meeting(APIView):
    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        if post.helper == None:
            timeDiff = datetime.datetime.now(datetime.timezone.utc)-post.created_at
            timeDiff = timeDiff.total_seconds()
            timeDiff = int(timeDiff)
            return Response({"min" : timeDiff // 60, "sec" : timeDiff % 60})
        else:
            if request.user == post.asker:
                user = User.objects.get(id=post.helper.id)
                post = Post.objects.get(id=post_id)
                serializer = HelperSerializer({"post": post, "helper": user})
                return Response(serializer.data)
            else:
                user = User.objects.get(id=post.asker.id)
                post = Post.objects.get(id=post_id)
                serializer = AskerSerializer({"post": post, "asker": user})
                return Response(serializer.data)
    
    def post(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        command = request.data['command']       
        if command == 'cancel':
            if request.user == post.helper:
                post.helper_confirm = False
                post.save()
            else:
                post.asker_confirm = False
                post.save()
        elif command == 'complete':
            if request.user == post.helper:
                post.helper_confirm = True
                post.save()
            else :
                post.asker_confirm = True
                post.save()
        elif command =='retry':
            post.helper = None
            post.helper_confirm = None
            post.asker_confirm = None
            post.save()
            return Response({'result': 'retry success'})
        elif command == 'remove':
            post.delete()
            return Response({'result': 'remove success'})
        else:
            return Response({'result': 'error'})
        
        if post.helper_confirm == True and post.asker_confirm == True:
            user = User.objects.get(id=post.helper.id)
            user.point += 500
            user.save()
                
        serializer = PostSerializer(post)
        return Response(serializer.data)
        
class MeetingAfter(APIView):  
    def post(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        if post.asker == request.user:
            review = Review.objects.create(post=post, asker = request.user, helper = post.helper, score=request.data['score'], content=request.data['content'])
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

class MainAsker(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

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
        post = Post.objects.create(category=category_name, location_latitude=float(latitude), location_longtitude=float(longtitude), 
                                   asker=request.user, helper=None, building_name=building_name, address=address,
                                   voice_record_name=voice_record_name)
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
class Reqconfirm(APIView):
    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
class GetPostInfo(APIView):
    def get(self, request, format=None):
        post = Post.objects.get(asker = request.user)
        serializer = PostSerializer(post, many = True)
        return Response(serializer.data)
