from django.shortcuts import render, HttpResponse
from django.db.models import Sum

from .models import Order, ExchangeRate


def index(request): 
    res = Order.objects.filter().values('date').order_by('date').annotate(sum=Sum('price_usd')) 
    return HttpResponse(res)