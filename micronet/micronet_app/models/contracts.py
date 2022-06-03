from django.db import models
from .providers import Provider
import datetime


class Contracts(models.Model):
    provider = models.ForeignKey(Provider,
                                on_delete=models.CASCADE)
    contract_id = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    status = models.CharField(max_length=225)
    createdAt = models.DateTimeField(default=datetime.datetime.today)
    balanceUnit = models.CharField(max_length=225)
    balance = models.IntegerField()
    kind = models.CharField(max_length=225)
    workspaceId = models.CharField(max_length=225)

    def addContract(self):
        self.save()

    @staticmethod
    def get_contracts(contract_id):
        return Contracts.objects.filter(contract_id=contract_id).order_by('-date')

