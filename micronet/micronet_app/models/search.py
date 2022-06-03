from django.db import models
from .providers import Provider
from .contracts import Contracts
from django.contrib.auth.models import User
import datetime


class Search(models.Model):
    search_id = models.CharField(max_length=250)
    user = models.ForeignKey(User,
                                on_delete=models.CASCADE)
    provider = models.CharField(max_length=50, default='')
    aoi = models.JSONField()
    products = models.JSONField()
    est_cost = models.FloatField()
    curr_unit = models.CharField(max_length=50, default='')
    
    def addSearch(self):
        self.save()