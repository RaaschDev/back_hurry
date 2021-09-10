from django.db import models
from apps.events.models import EventModel
from apps.base.models import BankData, Base


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
