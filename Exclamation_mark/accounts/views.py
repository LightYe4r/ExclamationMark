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
                'access_token': str(token.access_token)
            })
        
# TODO: implement
class Register(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.create( username=request.data['username'], 
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
    
class MainHelper(APIView):
    def get(self, request, format=None):
        posts = Post.objects.filter(helper=None)
        askers = posts.objects.select_related('asker').all()
        serializer = AskerSerializer({"posts": posts, "askers": askers}, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        post_id = request.data['post_id']
        post = Post.objects.get(id=post_id)
        post.helper = request.user
        post.save()
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
        if post.isWorkDone == False:
            return Response({'result': 'helper not complete'})
        else:
            user = User.objects.get(id=post.helper.id)
            return Response({'result': 'helper complete', "helper": UserSerializer(user).data})
    
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
            helper.point += 500
            helper.save()
            return Response({'result': 'review success'})

class MainAsker(APIView):
    def get(self, request, format=None):
        category_name = request.data['category_name']
        if category_name == 'all':
            posts = Post.objects.all()
        else:
            posts = Post.objects.filter(category=category_name)
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