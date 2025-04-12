from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from transaction.models import Transaction


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, telegram_id, username=None, password=None):
        if not telegram_id:
            raise ValueError('Users must have a telegram_id')
        user = self.model(
            telegram_id=telegram_id,
            username=username,
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, username=None, password=None):
        user = self.create_user(
            telegram_id,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.CharField(max_length=64, unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    balance = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    steam_trade_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    referer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def add_balance(self, amount):
        self.balance += amount
        self.save()

        Transaction.objects.create(
            user=self,
            transaction_type=Transaction.TransactionType.REWARD,
            amount=amount,
        )

    def spend_balance(self, amount):
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.save()
        Transaction.objects.create(
            user=self,
            transaction_type=Transaction.TransactionType.CASE_PURCHASE,
            amount=-amount,
        )

    def __str__(self):
        return f"{self.telegram_id}"
