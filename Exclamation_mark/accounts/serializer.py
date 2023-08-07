import rest_framework.serializers as serializers
from .models import User, Post

# Register your models here.
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'caller', 'title',  'location_latitude', 'location_longitude', 'category']