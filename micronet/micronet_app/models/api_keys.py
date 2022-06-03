from pydoc import describe
from django.db import models
from .providers import Provider
import datetime


class Apikeys(models.Model):
    date = models.DateTimeField(default=datetime.datetime.today)
    description = models.JSONField()
    expirationDate = models.DateTimeField(default=datetime.datetime.today)
    id = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)


    def addApikeys(self):
        self.save()

    # @staticmethod
    # def get_subscriptions_by_contracts(contract_id):
    #     return Contracts.objects.filter(customer=contract_id).order_by('-date')

