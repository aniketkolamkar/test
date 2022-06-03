from django.db import models
from django.contrib.postgres.fields import ArrayField
# from .search import Search
# from .customer import Customer
# import datetime
from django.contrib.postgres.fields import ArrayField
from time import gmtime, strftime


class Order(models.Model):
    order_id = models.CharField(max_length=50, default='', blank=False)
    kind = models.CharField (max_length=50, default='', blank=True)
    products = ArrayField(models.JSONField())
    customer_id = models.CharField(max_length=50, default='', blank=False)
    aoi = models.CharField(max_length=50, default='', blank=False)
    provider_name = models.CharField(max_length=50, default='', blank=False)
    promotion_id = models.CharField(max_length=50, default='', blank=False)
    order_date = models.DateTimeField(default=strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    type = models.CharField(max_length=50, default='', blank=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id)

