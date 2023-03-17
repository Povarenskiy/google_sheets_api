from django.db import models
from django.conf import settings


class Order(models.Model):
    """Модель заказа"""
    number = models.IntegerField()
    price_usd = models.IntegerField(null=True)
    price_rub = models.FloatField(null=True)
    date = models.DateField(null=True)

    class Meta:
       indexes = [
           models.Index(fields=['number'])]
       

class ExchangeRate(models.Model):
    value = models.FloatField()