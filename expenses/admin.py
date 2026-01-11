from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'category', 'entry_date', 'payment_method']
    list_filter = ['entry_date', 'payment_method', 'category']
    search_fields = ['title', 'description', 'category__name']
    ordering = ['-entry_date']
