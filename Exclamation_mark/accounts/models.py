from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
# Create your models here.

class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(username, email, password, **extra_fields)
    
class User(AbstractUser):
    name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    age = models.IntegerField(null=True)
    objects = UserManager()

class Mark(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caller')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    detail = models.TextField()