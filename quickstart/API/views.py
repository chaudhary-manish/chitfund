from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
#from quickstart.models import UserDetails,UserGroup
from quickstart.API.serializer import *
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from quickstart.models import *


class UserGroup(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):

    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserGroupSerializer
    queryset = UserGroup.objects.all()
    lookup_field = 'id'
    

    def get_queryset(self):
        return self.queryset.filter(createBy=self.request.user,isActive=1)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(createBy=self.request.user)

    def put(self, request, id=None):
        return self.update(request, id)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)        

    def delete(self, request, id=None):
        return self.destroy(request, id)


@api_view(['GET'])
def get_user_details(self,request):
    return Response(request)


@login_required(login_url="/login")
@api_view(['POST'])
def addgroupuser(request):
    data=request.data
    token = data['token']
    userid = Token.objects.get(key=token).user_id
    serializer = AddGroupUserSerializer(data=data,context={'user_id':userid})
    serializer.is_valid(raise_exception=True)
    return Response(token)


@login_required(login_url="/login")
@api_view(['GET', 'POST'])
def addgroup(request):
    if request.method == 'POST':
        data=request.data
        token = data['token']
        userid = Token.objects.get(key=token).user_id
        serializer = AddGroupSerializer(data=data,context={'user_id':userid})
        serializer.is_valid(raise_exception=True)
        return Response(token)
    
@login_required(login_url="/login/")
@api_view(['POST'])
def logout_user(request):
    logout(request)
    return  Response('Logout Successfully')


@api_view(['POST'])
def add_user_details(request):
    data=request.data
    #return Response(data)
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=200)


@api_view(['POST'])
def login_user(request):
    data=request.data
    #return Response(data)
    serializer = LoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    django_login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=200)
   
