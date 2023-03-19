from rest_framework import serializers
from .models import Tags
from .models import ImageInfo
from django.contrib.auth.models import User

class TagsSerializer(serializers.ModelSerializer):
    #外键字段的导入方法
    images = serializers.ReadOnlyField(source='images.image_name')
    class Meta:
        model = Tags
        # exclude = ('id',)排除字段
        # fields = ('id','tag_name','images')
        fields = '__all__'
        #外链遍历深度
        depth = 1 
'''
图片上传序列化
'''     
class ImageInfoSerializer(serializers.ModelSerializer):
    #外键字段的导入方法
    # images = serializers.ReadOnlyField(source='images.image_name',many=True)
    class Meta:
        model = ImageInfo
        # exclude = ('id',)
        # fields = ('id','tag_name','images')
        fields = '__all__'
        #外链遍历深度
        depth = 2 
        
#带URL的HyperlinkedModelSerializer
# class TagsSerializer(serializers.HyperlinkedModelSerializer):
#     images = serializers.ReadOnlyCharField(source='images.image_name')
#     class Meta:
#         model = Tags
#         # exclude = ('id',)
#         #url是默认值，可在settings.py中设置URL_FIELD_NAME使全局生效
#         fields = ('id','url','tag_name','images')
#         # fields = '__all__'
'''
用户注册序列化
'''
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #exclude和field互斥
        exclude = ('first_name','last_name','email')
'''
用户登录序列化
'''
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ('username','password')
