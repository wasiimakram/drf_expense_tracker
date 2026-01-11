from django.urls import path
from .views import (
    ExpenseListAndCreateAPIView,
    ExpenseDetailAndUpdateAndDeleteAPIView,
    ExpenseExportAPIView,
    ExpenseImportAPIView
)

urlpatterns = [
    path('', ExpenseListAndCreateAPIView.as_view(), name='expense-list'),
    path('<int:pk>/', ExpenseDetailAndUpdateAndDeleteAPIView.as_view(), name='expense-detail'),
    path('export/', ExpenseExportAPIView.as_view(), name='expense-export'),
    path('import/', ExpenseImportAPIView.as_view(), name='expense-import'),
]
