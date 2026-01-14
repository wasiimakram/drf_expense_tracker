from rest_framework import generics, filters, pagination, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Expense
from categories.models import Category
from .serializers import ExpenseSerializer, ExpenseExportSerializer, ExpenseImportSerializer
from expense_tracker.utils import CustomPagination, parse_date, UserQuerySetMixin
from .import_export_helper import ExpenseCSVRenderer, process_expense_csv
from expense_tracker.permissions import IsManagerAdminOrOwner

class ExpenseListAndCreateAPIView(UserQuerySetMixin, generics.ListCreateAPIView):
    """
    API Endpoint: List and Create Expenses.
    Inherits 'UserQuerySetMixin' to ensure users only see their own records.
    
    - GET: Returns a paginated list of expenses. Supports filtering, searching, and ordering.
    - POST: Creates a new expense record. Input requires category ID.

    Features:
    - Pagination: Custom (Page size control via query param).
    - Filters: Category, Date, Payment Method.
    """
    # Optimization: Use select_related to fetch Category in the same SQL query (Avoid N+1 problem)
    queryset = Expense.objects.select_related('category').all()
    serializer_class = ExpenseSerializer
    pagination_class = CustomPagination
    # Apply Custom Permission: Managers (Read All), Admin (Delete All), Owner (Full Access)
    permission_classes = [permissions.IsAuthenticated, IsManagerAdminOrOwner]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'payment_method', 'entry_date']
    search_fields = ['title', 'description']
    ordering_fields = ['amount', 'entry_date', 'created_at']
    ordering = ['-entry_date']

    # Example URL calls:
    # Filtering: ?category=Food&payment_method=Cash&entry_date=2023-10-27
    # Searching: ?search=coffee
    # Ordering:  ?ordering=-amount (Descending) or ?ordering=amount (Ascending)
    # Combined:  ?category=Food&search=starbucks&ordering=-entry_date


class ExpenseDetailAndUpdateAndDeleteAPIView(UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    API Endpoint: Retrieve, Update, and Delete a specific Expense.
    
    Methods:
    - GET: Retrieve detailed info of a single expense (ID required).
    - PUT/PATCH: Update an existing expense.
    - DELETE: Remove an expense.
    """
    queryset = Expense.objects.select_related('category').all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerAdminOrOwner]


class ExpenseExportAPIView(UserQuerySetMixin, generics.ListAPIView):
    """
    API Endpoint: Export Expenses to CSV.
    
    Methods:
    - GET: Downloads a 'expenses.csv' file containing filtered data.
    
    Features:
    - Reuses the same filters as the List View (so users export what they see).
    - Uses 'ExpenseCSVRenderer' for custom column formatting.
    - Pagination is DISABLED to export the full dataset.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseExportSerializer
    renderer_classes = [ExpenseCSVRenderer] # Use our custom class for export
    pagination_class = None # Export ALL data, not just one page
    permission_classes = [permissions.IsAuthenticated]
    
    # Reuse valid filters for export
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'payment_method', 'entry_date']
    search_fields = ['title', 'description']
    ordering_fields = ['amount', 'entry_date', 'created_at']
    ordering = ['-entry_date']

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Interceptor to add the 'Content-Disposition' header, forcing the 
        browser to treat the response as a file download.
        """
        response = super().finalize_response(request, response, *args, **kwargs)
        # Content-Disposition tells the browser "This is a file attachment"
        response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
        return response


class ExpenseImportAPIView(generics.GenericAPIView):
    """
    API Endpoint: Bulk Import Expenses from CSV.
    
    Methods:
    - POST: Upload a CSV file `file` form-data field.
    
    Logic:
    - Validates file type (.csv).
    - Parses CSV rows and matches Categories by name (case-insensitive).
    - Creates valid records and reports errors for invalid rows.
    """
    serializer_class = ExpenseImportSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # 1. Validate the file upload container
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file_obj = serializer.validated_data['file']
        
        # 2. Process the file contents using our helper service
        result = process_expense_csv(file_obj, request.user)

        # 3. Return the summary report
        return Response(result, status=status.HTTP_201_CREATED)
