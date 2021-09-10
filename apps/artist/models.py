from django.db import models
from apps.events.models import EventModel
from apps.base.models import Base


class ArtistModel(Base):
    description = models.CharField(max_length=155)
    spotfy = models.URLField()
    start = models.CharField(max_length=5)
    end = models.CharField(max_length=5)
    img = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, related_name='artists_id')

    def __str__(self):
        return self.description
