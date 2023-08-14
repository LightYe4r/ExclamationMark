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
    name = models.CharField(max_length=50, null=True)
    type_choices = (
        ('caller', 'caller'),
        ('receiver', 'receiver'),
    )
    type = models.CharField(max_length=8, choices=type_choices, null=False)
    phone_number = models.CharField(max_length=11, null=True)
    age = models.IntegerField(null=True)
    objects = UserManager()

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caller')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=True, blank=True)
    title = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    location_latitude = models.FloatField(null=False)
    location_longitude = models.FloatField(null=False)
    # category_choices = (
    #     [(int(i), int(i)) for i in range(1, 11)]
    # )
    # category = models.IntegerField(null=False, choices=category_choices)
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
    
    #주소명, 건물명 추가

# class PostManager(models.Manager):
#     def create(self, caller, title, location_latitude, location_longitude, category):
#         post = self.model(
#             caller = request.user.username,
#             title = title,
#             location_latitude = location_latitude,
#             location_longitude = location_longitude,
#             category = category
#         )
#         post.save()
#         return post