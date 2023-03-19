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
from .serializers import TagsSerializer,ImageInfoSerializer,UserRegisterSerializer,LoginSerializer
from django.http import JsonResponse 
import json
from django.forms import model_to_dict
from django.contrib import auth
import os
#Django的信号机制

# Create your views here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender,instance=None,created=False,**kwargs):
    '''
    创建用户时自动生成Token
    '''
    if created:
        Token.objects.create(user=instance)

'''
DRF的视图集viewsets编写API的测试方法
'''


class  TagsViewSets(viewsets.ModelViewSet):
    
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    # def perform_create(self, serializer):
    #     serializer.save(images=self.request.tag_name)
    # permission_classes(IsAuthenticated,IsOwnerReadOnly)
    

class  ImageTagsViewSets(viewsets.ModelViewSet):
    #只有登录才能进行操作
    permission_classes=(IsAuthenticated,)
    queryset = ImageInfo.objects.all()
    serializer_class = ImageInfoSerializer
    def retrieve(self,request,pk):
        res={}
        key=pk
        img = ImageInfo.objects.get(id=pk)
        img = img.tags_set.all()
        # print(img[0].id)
        # img=json.dumps(list(img.values()))
        # img = model_to_dict(img.tags_set.all().first())
        res['list']=json.loads(serializers.serialize('json', img))
        # print(type(res['list'][0]['fields'].values()))
        res=res['list'][0]['fields']
        # res=dict([(key,res['list'][0]['fields'][key])for key in['id','tag_name']])
        # print(res)
        return JsonResponse(res,safe=False)
'''
视图集方法重写的对应关系：
"get": "retrieve",
"post":"create"
"put": "update",(全部更新)
"patch": "partial_update",(部分更新)
"delete":"destroy",
'''

