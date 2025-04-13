import uuid
from django.db import models
from django.conf import settings
from cases.models import CaseItem

# Create your models here.
User = settings.AUTH_USER_MODEL

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        CASE_PURCHASE = 'case_purchase', 'Case Purchase'
        ITEM_DROP = 'item_drop', 'Item Drop'
        STEAM_TRADE = 'steam_trade', 'Steam Trade'
        REWARD = 'reward', 'Reward'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices,
                                        verbose_name="Transaction Type")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(CaseItem, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.transaction_type} - {self.amount} - {self.created_at}"
