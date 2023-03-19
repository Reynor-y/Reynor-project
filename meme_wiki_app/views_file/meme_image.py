from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.shortcuts import render,HttpResponse
from django.core import serializers
from django.http import HttpResponse
from meme_wiki_app.models import ImageInfo,Tags

from rest_framework import viewsets,status
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
import os
import random
import string
import re
'''
图片上传模块
'''
class  ImageUpload(viewsets.ModelViewSet):
    serializer_class = ImageInfoSerializer
    queryset = Tags.objects.all()
    def create(self,request):
        image = request.FILES.get('file')
        file_name = 'meme_image\\'
        random_str = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
        image_name = file_name+image.name+random_str
        url = os.path.join(settings.MEDIA_ROOT,image_name)
        f = open(url,'wb')
        for chunk in image.chunks():
            f.write(chunk)
        f.close()
        user = request.user
        auth.login(request, user)
        image = ImageInfo(src=url,upload_user=user,)
        image.save()
        #获取输入的标签并建立多对多关系
        if request.POST.get('tags'):
            #从POST的数据中获取用分号分割的多个标签
            tags = request.POST.get('tags').split(';')
            print(tags)
            for count,value in enumerate(tags):
                print(count)
                tag = Tags(tag_name=value)
                tag_queryset = Tags.objects.filter(tag_name=value)
                '''
                由于自动建立多对多关系需要利用save()获取id
                所以当所存储数据已存在且不能重复时
                需要查询已有的id，手动赋值给要保存的对象
                '''
                if tag_queryset.exists():
                    tag.id = tag_queryset.values('id')[0]['id']
                    tag.save()
                    tag.images.add(image)
                else:
                    tag.save()
                    tag.images.add(image)
                    # image.tags_set.add(tag)
                # print(image.tags_set.all()[count].tag_name)
                # print(tag.images.all()[0].id)
        else:
            return HttpResponse('没有标签')
        return HttpResponse('success')
'''
图片删除模块
'''
class  ImageDelete(viewsets.ModelViewSet):
    # permission_classes=(IsAuthenticated,)
    serializer_class = ImageInfoSerializer
    queryset = ImageInfo.objects.all()
    def retrieve(self,request,pk):
        ImageInfo.objects.delete(id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
图片搜索模块
'''
class ImageSearch(viewsets.ModelViewSet):
    serializer_class = ImageInfoSerializer
    queryset = ImageInfo.objects.all()
    def retrieve(self, request):
        search_tag = request.GET.get('tag')
        search_regex = r'\w*%s\w*'%(search_tag)
        print(search_regex)
        # search_tag_obj = ImageInfo.objects.filter(tags__tag_name__iregex=search_regex)
        search_image_obj = ImageInfo.objects.filter(tags__tag_name__iregex=search_regex)
        '''
        #使用values方法获取model对象的所有值或所选字段的值
        # result = search_tag_obj.values('tag_name')
        #使用values_list方法获取model对象的所有值
        result = search_tag_obj.values_list('tag_name')
        print(search_tag_obj)
        print(result)
        #通过多对多关系反向查询（从没有多对多字段的表）
        search_tag_obj = ImageInfo.objects.filter(tags__tag_name=search_tag)[1]
        '''
        result = search_image_obj.values_list('src')
        # result = search_tag_obj.all()
        # print(search_tag_obj)
        print(result)
        
        return HttpResponse('success')