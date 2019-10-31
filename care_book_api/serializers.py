from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User

from .models import Child, Allergy

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class SignupSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(required=True)


class UserInviteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ["email"]
       
    def create(self, validated_data):
        User.objects.create(
            username = validated_data["email"],
            email = validated_data["email"],
            password = ""
        )
        return validated_data


class AddChildSerializer(serializers.ModelSerializer):
    print("I AM ALLERGY")
    print(Allergy.objects.all())
    allergies = serializers.SlugRelatedField(
        many=True, 
        queryset=Allergy.objects.all(),
        slug_field='name',
    )
    class Meta:
        model = Child
        fields = ["name", "image", "dob", "medical_history","allergies"]