from django.urls import path

from fintrack.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]