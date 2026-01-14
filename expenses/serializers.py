from rest_framework import serializers
from django.utils import timezone
from .models import Expense
from categories.models import Category

from categories.serializers import CategorySerializer

class ExpenseAgainstCategorySerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for embedding Expenses inside other resources (like Categories).
    Does NOT include nested Category info to avoid circular recursion.
    """
    class Meta:
        model = Expense
        fields = ['id', 'title', 'amount', 'entry_date']

class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for Expense model.
    """
    # Nested serializer for category details
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 
            'title', 
            'category',
            'category_detail', 
            'amount', 
            'entry_date', 
            'payment_method', 
            'description', 
            'supporting_document', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_amount(self, value):
        """
        Amount must be positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class ExpenseExportSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_type = serializers.CharField(source='category.type', read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id',
            'title',
            'amount',
            'category_name',
            'category_type',
            'entry_date',
            'payment_method',
            'description',
            'created_at'
        ]


    def validate_entry_date(self, value):
        """
        Entry date cannot be in the future.
        """
        if value > timezone.now().date():
            raise serializers.ValidationError("Entry date cannot be in the future.")
        return value

    def validate_category(self, value):
        """
        Ensure selected category is actually an 'expense' category.
        """
        if value.type != 'expense':
            raise serializers.ValidationError(
                f"Invalid category '{value.name}'. It must be an 'expense' category."
            )
        return value


class ExpenseImportSerializer(serializers.Serializer):
    # We have added validations in view level. Because its very complex to read file in serliazers.
    # Serilizers are mostly used for simple check and JSON formats, not looping etc.
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        return value

