from django.urls import path, re_path

from fintrack.views import HomePageView, TransactionListJson, TransactionPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('transactions/', TransactionPageView.as_view(), name='transactions'),
    re_path(r'^datatable/data/$', TransactionListJson.as_view(), name='transactions-list'),
]
