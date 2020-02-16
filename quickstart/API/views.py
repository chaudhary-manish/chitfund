from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from quickstart.models import UserDetails,UserGroup
from quickstart.API.serializer import *
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login as django_login, logout as django_logout

@api_view(['GET'])
def get_user_details(self,request):
    return Response(request)



@login_required(login_url="/login")
@api_view(['POST'])
def addgroup(request):
    context = {}
    context['user'] = 'manish'
    return Response(context['user'])

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
   
