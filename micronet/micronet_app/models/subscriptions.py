from django.db import models
from .providers import Provider
from .contracts import Contracts
import datetime
from django.contrib.postgres.fields import ArrayField


class Subscriptions(models.Model):
    provider = models.ForeignKey(Provider,
                                on_delete=models.CASCADE,default=0)
    subscription_id = models.CharField(max_length=250)
    serviceinfo = models.JSONField()
    status = models.CharField(max_length=250)
    startedAt = models.DateTimeField(null=True,default="2012-09-04 06:00:00.000000-08:00")
    endedAt = models.DurationField (null=True,default="2012-09-04 06:00:00.000000-08:00")
    type = models.CharField(max_length=250)

    def addSubscriptions(self):
        self.save()

    @staticmethod
    def get_subscriptions(subscription_id):
        return Contracts.objects.filter(subscription_id=subscription_id).order_by('-date')

