from django.db import models

class Provider(models.Model):
    provider_name = models.CharField(max_length=250)
    label = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    api_key = models.CharField(max_length=250)
    links = models.JSONField()
    
    def addProvider(self):
        self.save()

    
    