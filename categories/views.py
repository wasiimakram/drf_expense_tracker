from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
from .serializers import CategorySerializer
from expense_tracker.utils import UserQuerySetMixin


class CategoryListAndCreateAPIView(UserQuerySetMixin, generics.ListCreateAPIView):
    """
    GET: List all categories (scoped to user via UserQuerySetMixin)
    POST: Create new category (auto-assigns user)
    """
    # Filter by type (as query param) - income/expense
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']
    
    queryset = Category.objects.all() # Base queryset, refined by Mixin
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryDetailAndUpdateAndDeleteAPIView(UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve specific category
    PUT/PATCH: Update category
    DELETE: Delete category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]