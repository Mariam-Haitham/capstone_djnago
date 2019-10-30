from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User

from .models import Allergy, Child, Post, Home

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Home
        fields= '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
    
#     class Meta:
#         model = Profile
#         fields = ["user", "number", "bio", "image"]

#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user')
#         user_serializer = UserSerializer()
#         super().update(instance, validated_data)
#         super(UserSerializer, user_serializer).update(instance.user,user_data)
#         return instance