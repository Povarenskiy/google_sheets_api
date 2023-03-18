import time
import requests


from google_sheets_api.celery import app
from celery.signals import celeryd_init
from django.conf import settings
from datetime import datetime

from .models import Order, ExchangeRate
from .services import _get_google_client, _get_exchange_rate


@app.task
def get_exchange_rate_task():
    """
    Периодическая задача Celery.
    Обновление курса $.
    """
    return _get_exchange_rate


@app.task
def send_notification():
    """
    Периодическая задача celery. 
    Рассылка уведомлений об окончании срока доставки заказов.
    """
    apiURL = f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage'

    get_message = lambda n, d: f'Срок поставки заказа {n} истек {d} сегодня.'
    message = '\n'.join([get_message(order.number, order.date) for order in Order.objects.filter(date__lt=datetime.now())])
    
    try:
        requests.post(apiURL, json={'chat_id': settings.CHAT_ID, 'text': message})
    except Exception as e:
        print(f'Отправка сообщений не удалась, причина: {e}')


@app.task
def write_sheet_data():
    """
    Задача celery. 
    Синхроницазая базы данных Order с таблицей Google Sheets.
    """
    client = _get_google_client()       # клиент Google Api

    while True:
        # Получаем обменный курс
        try:
            exchange_rate = ExchangeRate.objects.get()
        except ExchangeRate.DoesNotExist:
            exchange_rate = _get_exchange_rate()
        
        # Получаем данные по заказам из документа Google Sheets
        doc = client.open_by_key(settings.DOC)
        sheet = doc.worksheet(settings.SHEET).get_all_values()[1:]

        # Записываем все заказы из базы данных в словарь для сравнение таблицей Google Sheet    
        orders = {order.number: order for order in Order.objects.all()}

        for row in sheet:
            # Считываем данные построчно из таблицы
            number, price_usd, date = int(row[1]), int(row[2]), datetime.strptime(row[3], "%d.%m.%Y")
            # Ищем заказ в с соответствующим номером из таблицы
            order = orders.pop(number, None)
            
            # Существующие заказы перезаписываем, если они отличаются от данных в таблице.
            # Не существующие заказы записываем в базу данных.
            if order:   
                if number != order.number\
                or price_usd != order.price_usd\
                or date.strftime("%d.%m.%Y") != order.date.strftime("%d.%m.%Y"):
                    order.number = number
                    order.price_usd = price_usd
                    order.price_rub  = float(price_usd) * exchange_rate.rate
                    order.date = date
                    order.save()
            else:
                Order.objects.create(
                    number=number,
                    price_usd=price_usd, 
                    price_rub=float(price_usd) * exchange_rate.rate, 
                    date=date
                )
       
        # Если в словаре остались номера, значит данные заказы удалены из таблицы Google Sheet
        # Удаляем данные заказы из базы данных   
        if orders:
            Order.objects.filter(number__in=orders).delete()

        # Задержка для не превышения лимитов по количеству запросов (60 в минуту)
        time.sleep(2)


@celeryd_init.connect
def configure_workers(*args, **kwargs):
    """Запуск задачи celery при со старта"""
    write_sheet_data.delay() 

