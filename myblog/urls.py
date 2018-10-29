"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('test/', posts, name = "test"),
    path('post/', posts_list, name = "post_list_url"),
    path('post/create/', PostCreate.as_view(), name="post_create_url"),
    path('postdetail/<str:slug>/', Post_detail.as_view(), name="post_detail_url"),
    path('tag/', tag_list, name="tag_list_url"),
    path('tag/create/', TagCreate.as_view(), name="tag_create_url"),
    path('tagdetail/<str:slug>/', Tag_detail.as_view(), name="tag_detail_url"),

]
