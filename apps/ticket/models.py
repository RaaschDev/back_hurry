
from django.db.models.fields import DecimalField
from apps.wallet.models import Wallet
from django.db import models
from apps.base.models import Base
from apps.events.models import EventAnalitc, EventModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class TicketModel(Base):
    GENDER = (
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )
    description = models.CharField(max_length=155)
    batch = models.CharField(max_length=155)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER)
    status = models.BooleanField(default=False)
    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, related_name='tickets_id')

    def __str__(self):
        return self.description


class SaleT(Base):
    TYPE = (
        (1, "FULL"),
        (2, "HALF"),
    )
    ticket = ticket = models.ForeignKey(
        TicketModel, on_delete=models.PROTECT, related_name='sales')
    ticket_type = models.IntegerField(choices=TYPE)
    salesman = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='tickets_sales')
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='tickets_buyers')
    quantity = models.IntegerField()
    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        amount = 0
        if self.ticket_type != 1:
            amount = (self.quantity * self.ticket.price) / 2
        else:
            amount = self.quantity * self.ticket.price
        self.amount = amount
        self.event = self.ticket.event
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket.description


class TicketSale(models.Model):
    ticket = models.ForeignKey(
        TicketModel, on_delete=models.DO_NOTHING, blank=True, null=True)
    ticket_type = models.IntegerField()
    salesmen = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.DO_NOTHING, related_name="tickets", blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.ticket.description} - {self.ticket_type}"


def sale_ticket(sender, instance, *args, **kwargs):
    sale = instance
    ticket = sale.ticket
    ticket_type = sale.ticket_type
    salesmen = sale.salesman
    quantity = sale.quantity
    event = sale.event
    amount = sale.amount
    wallet = sale.wallet

    list = TicketSale.objects.filter(
        event=event, wallet=wallet, ticket_type=ticket_type)
    if len(list) == 0:
        TicketSale.objects.create(
            ticket=ticket,
            ticket_type=ticket_type,
            salesmen=salesmen,
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
    receiver=sale_ticket,
    sender=SaleT
)


def change_analitic_ticket(sender, instance, *args, **kwargs):
    sale = instance
    event = sale.event
    billing = sale.amount
    list = EventAnalitc.objects.filter(
        event=event)
    if len(list) == 0:
        EventAnalitc.objects.create(
            event=event,
            billing=billing
        )
    else:
        obj = list[0]
        obj.billing += billing
        obj.save()


post_save.connect(
    receiver=change_analitic_ticket,
    sender=SaleT
)
