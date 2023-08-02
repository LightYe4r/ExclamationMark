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
    post_id = models.AutoField(primary_key=True)
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caller')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=True)
    title = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    caller_location = models.CharField(max_length=50, null=False)
    category_choices = (
        [(str(i)+'번', str(i)+'번') for i in range(1, 11)]
    )
    category = models.CharField(max_length=3, choices=category_choices, null=False)