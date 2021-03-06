from uuid import uuid4
import random
from django.db import models

from .transaction import Transaction


class User(models.Model):

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    discord_id = models.CharField(max_length=255, unique=True)
    balance = models.BigIntegerField(default=0)
    locked = models.BigIntegerField(default=0)
    memo = models.CharField(max_length=255, unique=True)
    withdrawal_address = models.CharField(max_length=64, blank=True, null=True)

    def get_available_balance(self):
        return self.balance - self.locked

    def __str__(self):
        return f"User: {self.discord_id}; Balance: {self.balance}; Available: {self.get_available_balance()}"


# generate a random memo and check if its already taken.
# If taken, generate another memo again until we find a valid memo
def generate_memo(instance):

    while True:

        memo = str(random.randint(100000, 999999))

        if not User.objects.filter(memo=memo).exists():
            return memo


def pre_save_post_receiver(sender, instance, *args, **kwargs):

    if not instance.memo:
        instance.memo = generate_memo(instance)


# save the memo before the User model is saved with the unique memo
models.signals.pre_save.connect(pre_save_post_receiver, sender=User)


class UserTransactionHistory(models.Model):

    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'

    type_choices = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw')
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=255, choices=type_choices)
    amount = models.BigIntegerField()
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User: {self.user} - {self.type} - {self.amount}"
