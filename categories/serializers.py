from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    
    Laravel equivalent: API Resources (app/Http/Resources/CategoryResource.php)
    """
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    # Field level Validations
    def validate_name(self, value):
        """
        Validate name field:
        1. Required (not empty)
        2. Name must be unique (regardless of type)
        """
        # Check if name is empty
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        
        # Clean the value
        name = value.strip()
        
        # Check if name already exists (any type)
        query = Category.objects.filter(name=name)
        
        # Exclude for Update: exclude current instance
        if self.instance:  # Updating existing category
            query = query.exclude(pk=self.instance.pk)
        
        if query.exists():
            raise serializers.ValidationError(f"Category with name '{name}' already exists.")
        
        return name

class CategoryWithExpensesSerializer(CategorySerializer):
    """
    Shows Category + Nested Expenses.
    Uses SerializerMethodField to avoid Circular Imports and allow custom filtering.
    """
    """
    ARCHITECTURE NOTE:
    Why use SerializerMethodField instead of standard nested serializer?
    
    1. Circular Dependency: 'ExpenseSerializer' already imports 'CategorySerializer'. 
       If we import 'ExpenseSerializer' here at the top level, Python will crash with a recursion error.
    
    2. Solution: We use a 'SerializerMethodField' with a Local Import inside the method.
       This defers the import until runtime, bypassing the circular check.
       
    3. Optimization: We use the lightweight 'ExpenseAgainstCategorySerializer' to avoid sending too much data.
    """
    expenses = serializers.SerializerMethodField()
    
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['expenses']

    def get_expenses(self, obj):
        # Local Import to avoid circular check
        from expenses.serializers import ExpenseAgainstCategorySerializer
        
        # 1. Get Logged-in User
        request = self.context.get('request')
        if not request:
            return []
            
        # 2. Get Expenses (Optimized via prefetch_related in View)
        # We filter by owner to ensure data privacy (Row Level Security)
        # Even though prefetch fetches all, we filter list in Python memory (Cheap & Fast)
        expenses_qs = obj.expenses.all()
        user_expenses = [e for e in expenses_qs if e.owner_id == request.user.id]
        
        # 3. Serialize
        return ExpenseAgainstCategorySerializer(user_expenses, many=True).data