from django.contrib import admin
from .models import Order, ExchangeRate


admin.site.register(Order)
admin.site.register(ExchangeRate)