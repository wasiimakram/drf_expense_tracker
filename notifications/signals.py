from django.db.models.signals import post_save
from django.dispatch import receiver
from expenses.models import Expense
from .models import Notification

@receiver(post_save, sender=Expense)
def create_expense_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.owner,
            title="New Expense",
            message=f"You recorded an expense of ${instance.amount} for {instance.title}.",
        )