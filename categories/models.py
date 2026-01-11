from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Category model for both income and expense categorization.
    
    Laravel equivalent: Eloquent Model in app/Models/Category.php
    """
    
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        # Ensure category names are unique per type PER OWNER
        unique_together = [['name', 'type', 'owner']]
        ordering = ['type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
