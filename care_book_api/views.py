from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (CreateAPIView, 
RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from .models import Home, Child, Allergy
from .serializers import (MyTokenObtainPairSerializer, 
SignupSerializer, UserInviteSerializer, ChildSerializer, 
ChildDetailsSerializer, ChildListSerializer)
from .permissions import IsHomeParent, IsChildParent


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
    permission_classes = [IsAuthenticated, IsHomeParent, ]

    def post(self, request, home_id):
        serializer = UserInviteSerializer(data=request.data)

        if serializer.is_valid():
            home = Home.objects.get(id=home_id) 
            user = User.objects.filter(username=serializer.data["email"])
            if(not user):
                user = User.objects.create(
                    username =  serializer.data["email"],
                    email = serializer.data["email"],
                    password = ""
                )
                user.save()
            else: 
                user = user[0]
            home.caretakers.add(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddChild(CreateAPIView):
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticated, IsHomeParent, ]

    def post(self, request, home_id):
        serializer = ChildSerializer(data=request.data)

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


class ChildDetails(RetrieveAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'child_id'
    permission_classes = [IsAuthenticated, IsChildParent, ]


class ChildUpdate(RetrieveUpdateAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer 
    lookup_field = 'id'
    lookup_url_kwarg = 'child_id'
    permission_classes = [IsAuthenticated, IsChildParent, ]


class ChildList(ListAPIView):
    serializer_class = ChildListSerializer

    def get_queryset(self):
        home = Home.objects.get(id=self.kwargs['home_id'])
        return Child.objects.filter(home=home)

    permission_classes = [IsAuthenticated, IsHomeParent, ]