from django.urls import path
from .views import TelegramSimpleAuthView, AddBalanceView, GetProfileView

urlpatterns = [
    path('auth/telegram/', TelegramSimpleAuthView.as_view(), name='telegram-auth'),
    path('add-balance/', AddBalanceView.as_view(), name='add-balance'),
    path('get-me/', GetProfileView.as_view(), name='get-profile'),
]
