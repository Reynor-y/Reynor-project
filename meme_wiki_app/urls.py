from django.contrib import admin
from django.urls import path,include
from meme_wiki_app import views,views_file
from rest_framework.routers import DefaultRouter
from .views_file import account,meme_image

router=DefaultRouter()
'''
register()有两个强制参数：
1.prefix 用于这组路由的URL前缀
2.viewset 视图集类
'''
#对应register方法的path写法
router.register(prefix="Tags" , viewset=views.TagsViewSets)
router.register(prefix="ImageTags" , viewset=views.ImageTagsViewSets)

urlpatterns = [
    path("",include(router.urls)),
    path("TagsViewSets/", views.TagsViewSets.as_view(
        {
            "get": "list",
            "post": "create"
        }
    ),name="viewsets=list"),
    path("TagsViewSets/<int:pk>/", views.TagsViewSets.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete":"destroy",
        }
    ),name="viewsets=detail"),
    path("ImageTagsViewSets/", views.ImageTagsViewSets.as_view(
        {
            "get": "list",
            "post": "create"
        }
    ),name="viewsets=ImageTags"),
    path("ImageTagsViewSets/<int:pk>/", views.ImageTagsViewSets.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete":"destroy",
        }
    ),name="viewsets=ImageTags"),
    path("UserRegister/",account.UserRegister.as_view(
        {
            "get": "list",
            "post": "create"
        }
    ),name="viewsets=UserRegister"),
    path("Login/",account.Login.as_view(
        {
            "get": "list",
            "post": "create"
        }
    ),name="viewsets=Login"),
    path("ImageUpload/",meme_image.ImageUpload.as_view(
        {
            "get": "list",
            "post": "create"
        }
    ),name="viewsets=ImageUpload"),
    path("ImageDelete/<int:pk>/",meme_image.ImageDelete.as_view(
        {
            "get": "retrieve",
            "delete": "destroy"
        }
    ),name="viewsets=ImageDelete"),
    path("ImageSearch/",meme_image.ImageSearch.as_view(
        {
            "get": "retrieve"
        }
    ),name="viewsets=ImageSearch"),
]

