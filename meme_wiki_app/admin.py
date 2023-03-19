from django.contrib import admin
from .models import ImageInfo,Tags
# Register your models here.
@admin.register(ImageInfo)
class ImageInfoAdmin(admin.ModelAdmin):
    #元组只有一个元素时后面要加逗号
    list_display = ('src','upload_date','upload_user','likes')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    #元组只有一个元素时后面要加逗号
    list_display = ('tag_name',)