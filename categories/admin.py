from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for Category model.
    
    Laravel equivalent: Not needed - Laravel uses separate admin packages
    """
    list_display = ['name', 'type', 'is_active', 'created_at']
    list_filter = ['type', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['type', 'name']
