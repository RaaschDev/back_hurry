from django.db import models
from apps.base.models import Base
from apps.events.models import EventModel
from django.contrib.auth.models import User


class Pub(Base):
    description = models.CharField(max_length=155)
    user = models.ManyToManyField(User)
    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, related_name='pub_id')

    def __str__(self):
        return self.description
