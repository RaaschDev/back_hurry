from django.db import models
from apps.events.models import EventAnalitc, EventModel
from apps.base.models import BankData, Base
from django.db.models.signals import post_save


class Vendor(Base, BankData):

    STATUS = (
        ('open', 'OPEN'),
        ('paid', 'PAID'),
        ('late', 'LATE'),
    )

    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, related_name='vendors')
    description = models.CharField(max_length=155)
    type = models.CharField(max_length=155)
    status = models.CharField(max_length=4, choices=STATUS, default='open')
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.description


def change_analitic_vendor(sender, instance, *args, **kwargs):
    vendor = instance
    event = vendor.event
    investment = vendor.amount
    list = EventAnalitc.objects.filter(
        event=event)
    if len(list) == 0:
        EventAnalitc.objects.create(
            event=event,
            investment=investment
        )
    else:
        obj = list[0]
        obj.investment += investment
        obj.save()


post_save.connect(
    receiver=change_analitic_vendor,
    sender=Vendor
)
