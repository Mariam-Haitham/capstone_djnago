from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User

from .models import Child, Allergy

import math
from datetime import date

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


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        exclude = ["home"]


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ["name"]

class ChildDetailsSerializer(serializers.ModelSerializer):
    allergies = AllergySerializer(many=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = ["name", "image", "dob", "medical_history", "allergies", "age"]

    def get_age(self, obj):
        age = math.floor((date.today() - obj.dob).days / 365.2425)

        return "%d %s"%(age, "years") if age > 1 else "%d %s"%(age, "year")


class ChildListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        exclude = ["home"]


class HomeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]
