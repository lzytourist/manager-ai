from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from .models import Transaction


class HomePageView(TemplateView):
    template_name = 'fintrack/home.html'


class TransactionPageView(TemplateView):
    template_name = 'fintrack/transactions.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TransactionListJson(BaseDatatableView):
    model = Transaction
    columns = ['title', 'amount', 'transaction_type', 'created_at']
    order_columns = ['title', 'amount', '', 'created_at']
    max_display_length = 100

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_initial_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')

    # def filter_queryset(self, qs):
    #     search = self.request.GET.get('search[value]', None)
    #     if search:
    #         qs = qs.filter(title__icontains=search)
    #     return qs  # <- Make sure you return this
