from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Home, Child, Allergy, Post
from .serializers import (
    MyTokenObtainPairSerializer, HomeSerializer, HomeViewSerializer,
    AllergySerializer, SignupSerializer, UserInviteSerializer, 
    ChildSerializer, FeedSerializer   
)
from .permissions import IsHomeParent, IsChildParent

from .utils import send_email, decode_base64


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

    def post(self, request, home_id, type):
        serializer = UserInviteSerializer(data=request.data)

        if serializer.is_valid():
            home = Home.objects.get(id=home_id)
            user, created = User.objects.get_or_create(username=serializer.data["email"])
            if created:
                user.email = serializer.data['email']
                user.password = ""
                user.save()
            if type == "parent":
                home.parents.add(user)
            else:
                home.caretakers.add(user)
            send_email(request.user.first_name, request.user.last_name, 
                [user.email], type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = HomeViewSerializer

    def get_queryset(self):
        return Home.objects.filter(
            Q(parents = self.request.user) |
            Q(caretakers = self.request.user)).distinct()


class AddHome(CreateAPIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = HomeSerializer(data=request.data)

        if serializer.is_valid():
            home = Home.objects.create(name = serializer.data['name'])
            home.parents.add(request.user)
            home.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeDetails(APIView):
    permission_classes = [IsAuthenticated, IsHomeParent, ]

    def get(self, request, home_id):
        home = Home.objects.get(id=home_id)
        feeds = Post.objects.filter(children__in=home.children.all()).distinct()
        serializer = FeedSerializer(feeds, many=True, context={"request":request})
        return Response(serializer.data)

    def post(self, request, home_id):
        request.data['image'] = decode_base64(request.data['image'])
        
        temp = Post.objects.create(
            message="",
            image=request.data['image'])
        
        request.data['image'] = temp.image
        

        serializer = FeedSerializer(data=request.data)

        if serializer.is_valid(): 
            print(temp.image)
            feed = Post.objects.create(
                message=serializer.data['message'],
                image=temp.image)

            feed.children.set(serializer.data['children'])
            feed.save()
            temp.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
    def put(self, request, home_id):
        home = Home.objects.get(id=home_id)
        serializer = HomeSerializer(data=request.data, instance=home)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddChild(APIView):
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticated, IsHomeParent, ]

    def post(self, request, home_id):
        request.data['image'] = decode_base64(request.data['image'])
        
        tempHome = Home.objects.get(id=1)
        temp = Child.objects.create(
            name="",
            image=request.data['image'],
            dob="2019-11-10",
            medical_history="",
            home=tempHome)
        request.data['image'] = temp.image

        serializer = ChildSerializer(data=request.data)

        if serializer.is_valid():
            home = Home.objects.get(id=home_id)
            child = Child.objects.create(home = home, 
                name = serializer.data['name'], 
                image = temp.image, 
                dob = serializer.data['dob'],
                medical_history = serializer.data['medical_history'], 
            )
            child.allergies.set(serializer.data['allergies'])
            child.save()
            temp.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildUpdate(RetrieveUpdateAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer 
    lookup_field = 'id'
    lookup_url_kwarg = 'child_id'
    permission_classes = [IsAuthenticated, IsChildParent, ]


class Allergy(ListAPIView):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer 