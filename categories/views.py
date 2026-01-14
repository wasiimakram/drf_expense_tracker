from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
from .serializers import CategorySerializer, CategoryWithExpensesSerializer
from expense_tracker.utils import UserQuerySetMixin
from rest_framework.permissions import IsAuthenticated
from expense_tracker.permissions import IsManagerAdminOrOwner 


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
    permission_classes = [IsAuthenticated, IsManagerAdminOrOwner]


class CategoryDetailAndUpdateAndDeleteAPIView(UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve specific category
    PUT/PATCH: Update category
    DELETE: Delete category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsManagerAdminOrOwner]

class CategoryWithExpensesListAPIView(UserQuerySetMixin, generics.ListAPIView):
    """
    Advanced Endpoint: List Categories WITH their nested Expenses.
    Optimized uses 'prefetch_related' to fetch expenses in 1 batch query.
    """
    serializer_class = CategoryWithExpensesSerializer
    permission_classes = [IsAuthenticated, IsManagerAdminOrOwner]
    queryset = Category.objects.all() # Required base queryset for Mixin inheritance

    def get_queryset(self):
        # 1. Get base categories for this user
        queryset = super().get_queryset()
        
        # 2. Optimization: Prefetch 'expenses'
        # Since Categories are private (owned by user), all expenses inside are also owned by user.
        # We don't need complex filtering here.
        return queryset.prefetch_related('expenses')
