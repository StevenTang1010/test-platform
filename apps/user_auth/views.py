#!/usr/bin/python
# -*- coding:utf-8 _*-
"""
@author:TXU
@file:ldap_auth
@time:2022/02/07
@email:tao.xu2008@outlook.com
@description: JWT
"""
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.user_auth.serializers import MyTokenObtainPairSerializer

from apps.customized_drf import BaseViewSet, JsonResponse
from apps.user_auth.models import UserProfile
from apps.user_auth.serializers import UserProfileSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return JsonResponse(data={'message': 'logout success!', }, status=200)


class UserProfileViewSet(BaseViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().order_by('id')
