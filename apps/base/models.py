from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AddressBase(models.Model):
    street = models.CharField(max_length=140)
    number = models.IntegerField()
    complement = models.CharField(max_length=150, blank=True, null=True)
    district = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    status = models.BooleanField(default=False)
    zip = models.CharField(max_length=15)

    class Meta:
        abstract = True


class BankData(models.Model):
    bank_name = models.CharField(max_length=155)
    account = models.IntegerField()
    agency = models.IntegerField()
    digit = models.IntegerField()
