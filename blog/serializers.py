from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'
    read_only_fields = ['updated_at', 'created_at']

class BlogSerializer(serializers.ModelSerializer):
  comments = CommentSerializer(many=True, read_only=True)
  class Meta:
    model = Blog
    fields = '__all__'
    read_only_fields = ['updated_at', 'created_at']

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'password', 'first_name', 'last_name']
    extra_kwargs = {
      'password': {'write_only': True},
    }

class LoginSerializer(serializers.Serializer):
  username = serializers.EmailField()
  password = serializers.CharField(write_only=True)
