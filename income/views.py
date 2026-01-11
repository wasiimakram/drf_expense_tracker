from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Income
from .serializers import IncomeSerializer
from expense_tracker.utils import CustomPagination, UserQuerySetMixin

class IncomeListAndCreateAPIView(UserQuerySetMixin, generics.ListCreateAPIView):
    """
    API Endpoint: List and Create Income Records.
    Inherits 'UserQuerySetMixin' to data isolation (User vs Admin).
    
    - GET: Returns a paginated list of incomes.
    - POST: Creates a new income record.
    """
    # select_related will reduce n queries
    queryset = Income.objects.select_related('category').all()
    serializer_class = IncomeSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    
    # Filters Related

    # Enable Searching, Filtering, and Ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filter by specific fields (Exact match)
    filterset_fields = ['category', 'payment_method', 'entry_date']
    
    # Search by text fields (Partial match)
    search_fields = ['title', 'description']
    
    # Order by date or amount
    ordering_fields = ['amount', 'entry_date', 'created_at']
    ordering = ['-entry_date'] # Default newest first

    # Example API URLs:
    # Filter:   /api/income/?category=Salary
    # Search:   /api/income/?search=freelance
    # Ordering: /api/income/?ordering=-amount (Descending order)
    # Combined: /api/income/?category=Salary&search=bonus&ordering=-entry_date



class IncomeDetailAndUpdateAndDeleteAPIView(UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    API Endpoint: Retrieve, Update, Delete specific Income.
    """
    queryset = Income.objects.select_related('category').all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]
