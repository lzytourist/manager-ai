from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Transaction


@receiver(pre_save, sender=Transaction)
def update_current_balance(instance, **kwargs):
    """Updates the current balance of the transaction."""
    last_transaction = (Transaction.objects.filter(user_id=instance.user_id).exclude(pk=instance.pk)
                        .order_by('-created_at').first())

    instance.balance_after_transaction = instance.amount
    if last_transaction:
        if instance.transaction_type == Transaction.Type.BALANCE:
            instance.balance_after_transaction += last_transaction.balance_after_transaction
        else:
            instance.balance_after_transaction = last_transaction.balance_after_transaction - instance.amount
