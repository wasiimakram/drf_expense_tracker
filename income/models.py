from django.db import models
from categories.models import Category
from django.contrib.auth.models import User

class Income(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='incomes',
        limit_choices_to={'type': 'income'} 
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateField()
    payment_method = models.CharField(max_length=50, default='cash')
    description = models.TextField(blank=True, null=True)
    supporting_document = models.FileField(upload_to='income/documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

    class Meta:
        ordering = ['-entry_date']
