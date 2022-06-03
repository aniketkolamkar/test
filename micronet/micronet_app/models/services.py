from django.db import models
from .providers import Provider
import datetime


class Services(models.Model):
    provider = models.CharField(max_length=225)
    service_id = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    type = models.CharField(max_length=225)
    cost = models.IntegerField()
    currencyunit = models.CharField(max_length=225)