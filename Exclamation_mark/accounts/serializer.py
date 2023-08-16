import rest_framework.serializers as serializers
from .models import User, Post, Review

# Register your models here.
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
class AskerSerializer(serializers.Serializer):   
    post = PostSerializer(read_only=True)
    asker = UserSerializer(read_only=True)
    
class HelperSerializer(serializers.Serializer):
    post = PostSerializer(read_only=True)
    helper = UserSerializer(read_only=True)