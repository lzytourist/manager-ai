from django.forms.models import ModelForm

from .models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'description', 'amount', 'transaction_type']
