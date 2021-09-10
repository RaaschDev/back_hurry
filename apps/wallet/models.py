from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Wallet(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='wallet')

    def __str__(self):
        return f"{self.id} - {self.user.username}"


# def create_wallet(sender, instance, created, **kwargs):
#     Wallet.objects.create(user=instance)


# post_save.connect(
#     receiver=create_wallet,
#     sender=User
# )
