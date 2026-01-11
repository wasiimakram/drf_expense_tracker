from django.urls import path
from .views import (
    CategoryListAndCreateAPIView,
    CategoryDetailAndUpdateAndDeleteAPIView
)

urlpatterns = [
    # POST, GET List
    path('', CategoryListAndCreateAPIView.as_view(), name='category-list'),
    # GET, PUT, DELETE
    path('<int:pk>/', CategoryDetailAndUpdateAndDeleteAPIView.as_view(), name='category-detail'),

    # GET    /api/categories/
    # POST   /api/categories/
    # GET    /api/categories/<id>/
    # PUT    /api/categories/<id>/
    # DELETE /api/categories/<id>/

]