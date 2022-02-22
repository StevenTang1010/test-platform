# --------------------------------------
# Date: 2021/8/5
# @Author: Steven_Tang
# FileName: urls.py   
# Description: 
# --------------------------------------

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.bug_analysis.views import OrdersViewSet, StatisticsViewSet, AnalysisViewSet, BugTrendViewSet

router = DefaultRouter()

# 注册orders的url
router.register(r'list', OrdersViewSet, basename='list')
router.register(r'update', OrdersViewSet, basename='update')
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'trend', BugTrendViewSet, basename='BugTrend')
router.register(r'analysis', AnalysisViewSet, basename='analysis')
# router.register(r'export', ExportViewSet, basename='export')

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]