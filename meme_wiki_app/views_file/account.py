from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.shortcuts import render,HttpResponse
from django.core import serializers
from meme_wiki_app.models import ImageInfo,Tags

from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
#装饰器
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from ..serializers import TagsSerializer,ImageInfoSerializer,UserRegisterSerializer,LoginSerializer
from django.http import JsonResponse 
import json
from django.forms import model_to_dict
from django.contrib import auth

'''
用户注册模块
'''
class  UserRegister(viewsets.ModelViewSet):
    serializer_class = UserRegisterSerializer
    def create(self,request):
        #creatr_user可以快速创建用户，username,email,password这三个参数必须传递
        #当前端传回json数据时，不能直接使用request.POST.get()
        data=json.loads(request.body)
        username=data.get('username')
        email=data.get('email')
        password=data.get('password')
        # User.objects.create_user(username=request.POST.get('username'),email=request.POST.get('email'),password=request.POST.get('password'))
        User.objects.create_user(username=username,email=email,password=password)
        
        return HttpResponse('success')
    
'''
用户登录模块
'''
class Login(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    def create(self,request):
        data=json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = auth.authenticate(request,username=username, password=password)
        if user:
            auth.login(request, user)
            print(request.user)
            return HttpResponse('success')
        else:
            return HttpResponse('不能为空')