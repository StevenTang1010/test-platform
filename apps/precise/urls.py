# --------------------------------------
# Date: 2021/8/23
# @Author: Steven_Tang
# FileName: urls.py   
# Description: 
# --------------------------------------

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

# 注册orders的url
router.register(r'system', SystemViewSet, basename='system')
router.register(r'primary', PrimaryViewSet, basename='primary')
router.register(r'second', SecondaryViewSet, basename='second')
router.register(r'third', ThirdViewSet, basename='third')
router.register(r'search', SearchViewSet, basename='search')
router.register(r'detail', DirectDetail, basename='detail')
router.register(r'func/match', MatchFunc, basename='func')
router.register(r'func/create', CreateFunc, basename='create')

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]
