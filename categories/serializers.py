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