import uuid
from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="case-images/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class CaseItem(models.Model):
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('very_rare', 'Very Rare'),
        ('legendary', 'Legendary'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="item-images/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rarity = models.CharField(max_length=10, choices=RARITY_CHOICES, default='common')
    chance = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.rarity})"


class UserInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(CaseItem, on_delete=models.CASCADE)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.name})"
