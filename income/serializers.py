from rest_framework import serializers
from .models import Income
from categories.serializers import CategorySerializer
from django.utils import timezone

class IncomeSerializer(serializers.ModelSerializer):
    # Nested serializer for rich response (Read-only)
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Income
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
        if value <= 0:
            raise serializers.ValidationError("Income amount must be positive.")
        return value

    def validate_entry_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Income date cannot be in the future.")
        return value
