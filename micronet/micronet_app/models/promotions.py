from django.db import models
from .providers import Provider
import datetime


class Promotions(models.Model):
    provider = models.CharField(max_length=225)
    promotion_id = models.CharField(max_length=225)
    promotype = models.CharField(max_length=225)
    start_date = models.DateTimeField(default=datetime.datetime.today)
    end_date = models.DateTimeField(default=datetime.datetime.today)