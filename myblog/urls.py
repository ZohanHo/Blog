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

from django.urls import path, include
from .views import *

urlpatterns = [
    path('test/', posts, name = "test"),
    path('post/',MyListViewPost.as_view() , name = "post_list_url"),   # posts_list
    path('post/create/', PostCreateView.as_view(), name="post_create_url"),
    path('post/<pk>/', PostDetailView.as_view(), name="post_detail_url"),
    path('post/<pk>/update/', PostUpdateViwe.as_view(), name="post_update_url"),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name="post_del_url"),
    path('tag/', MyListViewTag.as_view(), name="tag_list_url"), # tag_list
    path('tag/create/', TagCreate.as_view(), name="tag_create_url"),
    path('tag/<pk>/', TagDetailView.as_view(), name="tag_detail_url"),
    path('tag/<pk>/update/', TagUpdate.as_view(), name="tag_update_url"),
    path('tag/<pk>/delete/', TagDelete.as_view(), name="tag_del_url"),


]
