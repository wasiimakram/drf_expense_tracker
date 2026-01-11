from django.urls import path
from .views import (
    IncomeListAndCreateAPIView,
    IncomeDetailAndUpdateAndDeleteAPIView
)

urlpatterns = [
    path('', IncomeListAndCreateAPIView.as_view(), name='income-list'),
    path('<int:pk>/', IncomeDetailAndUpdateAndDeleteAPIView.as_view(), name='income-detail'),
]
