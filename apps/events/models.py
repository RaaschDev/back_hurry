from django.db import models


from apps.base.models import AddressBase, Base


class EventTypeModel(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name


class Category(Base):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name


class EventModel(Base, AddressBase):
    description = models.CharField(max_length=155)
    date = models.DateField()
    start = models.CharField(max_length=5)
    end = models.CharField(max_length=5)
    event_type = models.ForeignKey(
        EventTypeModel, on_delete=models.DO_NOTHING, related_name='events')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='events')
    image = models.URLField()
    advertsing = models.URLField()
    status = models.BooleanField(default=False)
    commission = models.IntegerField(blank=True, null=True, default=0)
    investment = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.description


class EventAnalitc(models.Model):
    event = models.OneToOneField(
        EventModel, on_delete=models.DO_NOTHING, related_name='analitics')
    investment = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    billing = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    profit = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True, default=0)

    def __str__(self):
        return self.event.description
