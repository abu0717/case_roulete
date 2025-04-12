from django.urls import path
from .views import TransactionCreateView

urlpatterns = [
    path('transactions/', TransactionCreateView.as_view()),
]
