from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
# Create your models here.

class UserManager(DjangoUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(
            username = username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(username, password, **extra_fields)
    
    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(username, password, **extra_fields)

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, unique=True, null=False)
    type_choices = (
        ('asker', 'asker'),
        ('helper', 'helper'),
    )
    type = models.CharField(max_length=8, choices=type_choices, null=False)
    birth_Year = models.CharField(max_length=4,null=True)
    birth_Month = models.CharField(max_length=2,null=True)
    birth_Day = models.CharField(max_length=2,null=True)
    age = models.IntegerField(null=True)
    age_range = models.IntegerField(null=True)
    gender_choices = (
        ('male', '남성'),
        ('female', '여성'),
    )
    gender = models.CharField(max_length=7, choices=gender_choices, null=True)
    point = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    task_count = models.IntegerField(default=0)
    kind_count = models.IntegerField(default=0)
    easy_count = models.IntegerField(default=0)
    endure_count = models.IntegerField(default=0)
    fast_count = models.IntegerField(default=0)
    etc_count = models.IntegerField(default=0)
    user_latitude = models.FloatField(default = None, null = True, blank = True)
    user_longtitude = models.FloatField(default = None, null = True, blank = True)
    objects = UserManager()

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    asker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caller')
    helper = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=True, blank=True)
    title = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    location_latitude = models.FloatField(null=False)
    location_longtitude = models.FloatField(null=False)
    building_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    category_choices = (
        ('finance', '금융'),
        ('shopping', '쇼핑'),
        ('document_and_email', '문서 및 이메일 작성'),
        ('video_and_photo', '영상 및 사진'),
        ('reservation_and_booking', '예약 및 예매'),
        ('device_breakdown', '기기고장'),
        ('internet', '인터넷'),
        ('etc', '기타'),
    )
    category = models.CharField(max_length=25, null=False, choices=category_choices)
    voice_record_name = models.CharField(max_length=50, null=True, blank=True)
    asker_confirm = models.BooleanField(default=None, null=True, blank=True)
    helper_confirm = models.BooleanField(default=None, null=True, blank=True)

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    asker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asker')
    helper = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helper')
    score = models.FloatField(null=False)
    content_choices = (
        ('kind', '친절해요'),
        ('easy', '설명이쉬워요'),
        ('endure','인내심이깊어요'),
        ('fast', '빨라요'),
        ('etc', '기타'),
    )
    content = models.CharField(max_length=10, null=False, choices=content_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)