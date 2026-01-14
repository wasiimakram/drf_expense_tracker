from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import pagination
from datetime import datetime

def success_response(data=None, message="Success", status=200):
    """
    Standard success response format
    """
    return Response({
        "status": "success",
        "data": data,
        "message": message,
        "errors": None
    }, status=status)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for standardized error responses
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the response format
        custom_response = {
            "status": "error",
            "data": None,
            "message": "Validation failed" if response.status_code == 400 else "Error occurred",
            "errors": response.data
        }
        response.data = custom_response
    
    return response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


def parse_date(date_str):
    """
    Try parsing date from common formats.
    Supported: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY
    """
    if not date_str:
        return None
    
    date_str = date_str.strip()
    formats = [
        '%Y-%m-%d',       # 2026-01-05
        '%d/%m/%Y',       # 05/01/2026
        '%m/%d/%Y',       # 01/05/2026 (US)
        '%d-%m-%Y',       # 05-01-2026
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    raise ValueError(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD or DD/MM/YYYY.")


class UserQuerySetMixin:
    """
    Powerful Mixin to enforce 'Row Level Security' (RLS) in Views.
    
    1. get_queryset():
       - Admins & Managers -> See EVERYTHING (Global View).
       - Regular Users -> See ONLY their own data (filtered by 'owner').
    
    2. perform_create():
       - Automatically sets the 'owner' field to the current user when creating data.
    """
    user_field = 'owner'
    
    def get_queryset(self):
        # 1. Start with the base queryset (usually Model.objects.all())
        queryset = super().get_queryset()
        
        # 2. Get the user from the Request
        user = self.request.user
        
        # 3. SAFETY FIRST: If user is not logged in, return Nothing.
        # (Though 'permission_classes' should catch this, we double-check here)
        if not user.is_authenticated:
            return queryset.none()
            
        # 4. GLOBAL ACCESS: Check if User acts as an Admin or Manager
        is_admin = user.is_staff
        is_manager = user.groups.filter(name='Manager').exists()
        
        if is_admin or is_manager:
            return queryset # Return ALL records in the database
             
        # 5. PRIVATE ACCESS: Filter data to belong ONLY to this user
        # This translates to SQL: WHERE owner_id = user.id
        filter_kwargs = {self.user_field: user}
        return queryset.filter(**filter_kwargs)
    
    def perform_create(self, serializer):
        """
        Hook called during POST request.
        Manually injects the 'owner' field using the request.user.
        """
        serializer.save(**{self.user_field: self.request.user})

