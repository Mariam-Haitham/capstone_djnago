from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Home, Child, Allergy
from .serializers import (MyTokenObtainPairSerializer, SignupSerializer, 
UserInviteSerializer, AddChildSerializer)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class Signup(APIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.get_or_create(username=serializer.data["email"])
            user.first_name = serializer.data["first_name"]
            user.last_name = serializer.data["last_name"]
            user.email = serializer.data["email"]
            user.set_password(request.data['password'])
            user.save()
            if created:
                home = Home.objects.create()
                home.parents.add(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInvite(CreateAPIView):
    serializer_class = UserInviteSerializer
    permission_class = [IsAuthenticated]
    def post(self, request, home_id):
        serializer = UserInviteSerializer(data=request.data)

        if serializer.is_valid():
            home = Home.objects.get(id=home_id)
            req_user = User.objects.get(username=request.user)
            home_parent = home.parents.get(username=req_user)
            if(home_parent):
                user = User.objects.filter(username=serializer.data["email"])
                if(not user):
                    user = User.objects.create(
                        username =  serializer.data["email"],
                        email = serializer.data["email"],
                        password = ""
                    )
                    user.save()
                home.caretakers.add(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddChild(CreateAPIView):
    serializer_class = AddChildSerializer

    def post(self, request, home_id):
        serializer = AddChildSerializer(data=request.data)

        if serializer.is_valid():
            home = Home.objects.get(id=home_id)
            child = Child.objects.create(home = home, 
                name = serializer.data['name'], 
                image = serializer.data['image'], 
                dob = serializer.data['dob'],
                medical_history = serializer.data['medical_history'], 
            )
            child.allergies.set(serializer.data['allergies'])
            child.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       