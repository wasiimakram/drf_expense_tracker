from django.urls import path
from .views import DashboardSummaryAPIView, DashboardStatsAPIView

urlpatterns = [
    path('summary/', DashboardSummaryAPIView.as_view(), name='dashboard-summary'),
    path('stats/', DashboardStatsAPIView.as_view(), name='dashboard-stats'),
]
