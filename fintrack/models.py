from django.contrib.auth import get_user_model
from django.db import models


class Transaction(models.Model):
    class Type(models.TextChoices):
        BALANCE = 'balance', 'Balance'
        EXPENSE = 'expense', 'Expense'

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    transaction_type = models.CharField(max_length=10, choices=Type.choices)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
