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
    Mixin to filter queryset by the current user (owner).
    Superusers (Admin) can see all records.
    Also auto-assigns 'owner' field on create.
    """
    user_field = 'owner'
    
    def get_queryset(self):
        # Ensure we have a queryset from parent
        queryset = super().get_queryset()
        
        # Checking user from request (provided by JWT Auth)
        user = self.request.user
        
        # Safety check: if user is Anonymous (should be blocked by permission, but good to be safe)
        if not user.is_authenticated:
            return queryset.none()
            
        # Super Admin sees ALL (Global view)
        if user.is_staff:
             return queryset
             
        # Regular users see only their OWN data
        return queryset.filter(**{self.user_field: user}) # e.g. owner=user
    
    def perform_create(self, serializer):
        # Auto-assign the owner field to the logged-in user
        serializer.save(**{self.user_field: self.request.user})

