import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django_datatables_view.mixins import JSONResponseView

from .forms import TransactionForm
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
    columns = ['title', 'amount', 'transaction_type', 'created_at', 'description', 'id']
    order_columns = ['title', 'amount', '', 'created_at']
    max_display_length = 100

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TransactionDetail(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        transaction = Transaction.objects.filter(user=request.user).filter(pk=pk).values()
        return JsonResponse(data={
            'transaction': list(transaction)[0],
        })

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        transaction = Transaction.objects.filter(user=request.user).filter(pk=pk).first()
        form = TransactionForm(data=request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return JsonResponse(data={
                'message': 'Transaction saved',
            })
        return JsonResponse(data={
            'message': 'Transaction not saved',
            'errors': form.errors.as_json()
        }, status=400)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            Transaction.objects.filter(user=request.user).filter(pk=pk).delete()
            return JsonResponse(data={
                'message': 'Transaction deleted',
            })
        except Transaction.DoesNotExist as e:
            return JsonResponse(data={
                'message': 'Transaction not found',
            })
