from django.shortcuts import render, HttpResponse
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *


class OrderApiView(APIView):
    """Api для отображения информации о заказах"""
    def get(self, request):
        orders = Order.objects.all()

        # заказы для отображения в таблице
        orders_info = [
            {   
                'n': n + 1,
                'number': order.number,
                'price_usd': order.price_usd,
                'date': order.date,
            } for n, order in enumerate(orders[0:13])
        ]

        # аннотация для отображения на графике
        graph = orders.values('date').order_by('date').annotate(price_per_day=Sum('price_usd'))
        # агрегация для отображения суммаррной стоимости
        total = orders.aggregate(Sum('price_usd'))

        return Response({'total': total['price_usd__sum'], 'orders': orders_info, 'graph': graph})
