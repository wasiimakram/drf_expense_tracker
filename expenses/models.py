from django.db import models
from categories.models import Category
from django.contrib.auth.models import User

class Expense(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_payment', 'Mobile Payment'),
        ('other', 'Other'),
    ]
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE) # delete expenses when user deleted
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='expenses',
        limit_choices_to={'type': 'expense'}
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    description = models.TextField(blank=True, null=True)
    supporting_document = models.FileField(upload_to='expenses/documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-entry_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.amount}"
