"""testPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from rest_framework.schemas import get_schema_view
# from django.views.generic import TemplateView
from apps.system_manage import urls as system_manage_url
from apps.user_auth import urls as user_auth_url
from apps.api_test import urls as api_test_urls
from apps.bug_analysis import urls as order_url
from apps.precise import urls as precise_url

schema_view = get_schema_view(
    title='测试平台 API',
    # renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
    permission_classes=()
)
urlpatterns = [
    path('admin/', admin.site.urls),

    # 系统管理
    path('api/system_manage/', include(system_manage_url)),

    # 登录、注册、User维护： rest_framework_simplejwt | ldap
    path('api/user_auth/', include(user_auth_url)),

    # apps
    path('api/precise/', include(precise_url)),
    path('api/order/', include(order_url)),
    path('api_test/', include(api_test_urls)),
    path(r'docs/', schema_view, name="docs"),
]
