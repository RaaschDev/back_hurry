from django.db import models
from apps.base.models import Base
from apps.events.models import EventModel
from django.contrib.auth.models import User
from apps.wallet.models import Wallet
from django.db.models.signals import post_save


class Consumable(Base):
    CONSUMABLE = (
        ('drink', 'DRINK'),
        ('food', 'FOOD')
    )
    description = models.CharField(max_length=155)
    consumable_type = models.CharField(max_length=5, choices=CONSUMABLE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField('Quantity', default=1)
    img = models.URLField()
    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, related_name='consumables')

    def __str__(self):
        return self.description


class SaleC(Base):
    consumable = models.ForeignKey(
        Consumable, on_delete=models.PROTECT, related_name='sales')
    consumable_type = models.CharField(max_length=5, editable=False)
    salesman = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='consumables_sales')
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='consumable_buyers')
    quantity = models.IntegerField()
    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.consumable_type = self.consumable.consumable_type
        self.amount = self.quantity * self.consumable.price
        self.event = self.consumable.event
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.consumable.description


class ConsumableSale(models.Model):
    consumable = models.ForeignKey(
        Consumable, on_delete=models.DO_NOTHING, blank=True, null=True)
    consumable_type = models.CharField(max_length=5)
    salesman = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='consumables')
    quantity = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.consumable.description}"


def sale_consumable(sender, instance, *args, **kwargs):
    sale = instance
    consumable = sale.consumable
    consumable_type = sale.consumable_type
    salesman = sale.salesman
    quantity = sale.quantity
    event = sale.event
    amount = sale.amount
    wallet = sale.wallet
    list = ConsumableSale.objects.filter(
        event=event, wallet=wallet)
    if len(list) == 0:
        ConsumableSale.objects.create(
            consumable=consumable,
            consumable_type=consumable_type,
            salesman=salesman,
            quantity=quantity,
            event=event,
            amount=amount,
            wallet=wallet
        )
    else:
        obj = list[0]
        obj.amount += amount
        obj.quantity += quantity
        obj.save()


post_save.connect(
    receiver=sale_consumable,
    sender=SaleC
)
