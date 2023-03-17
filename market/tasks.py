import time
import gspread
import requests
import xml.etree.ElementTree as ET

from google.oauth2.service_account import Credentials
from google_sheets_api.celery import app
from celery.signals import celeryd_init
from celery import shared_task

from datetime import datetime
from .models import Order, ExchangeRate


def _get_google_client():
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    CREDS = Credentials.from_service_account_file('mypython-380810-49df9d8fa923.json', scopes=SCOPE)
    return gspread.authorize(CREDS)

    
@shared_task
def get_exchange_rate():
    """Запрос данных к ЦБ РФ  для перевода $ в рубли"""
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    root = ET.fromstring(response.text)
    value = float(root.find("Valute[@ID='R01235']/Value").text.replace(',', '.'))
    rate, is_created = ExchangeRate.objects.update_or_create(value=value)
    return rate

@app.task
def write_sheet_data():
    """Синхроницазая базы данных Order с таблицей Google Sheets"""
   
    # Настройки клиента для Google Sheets API
    doc_id = '13LcpN3xNXU0AGf9YI07CLy-DO3FDv3p9EO5VJpDJlHY'
    sheet_name = 'Лист1'
    client = _get_google_client()

    while True:
        # Получаем обменный курс
        print(time.time())
        try:
            exchange_rate = ExchangeRate.objects.get()
        except ExchangeRate.DoesNotExist:
            exchange_rate = get_exchange_rate()
        
        exchange_rate = exchange_rate.value
        
        # Открываем документ по его ID и получаем данные из нужного листа
        doc = client.open_by_key(doc_id)
        sheet = doc.worksheet(sheet_name).get_all_values()[1:]

        # записываем все заказы в словарь для сравнение с текущим состоянием таблицы Google Sheet    
        orders = {order.number: order for order in Order.objects.all()}

        for row in sheet:
            number, price_usd, date = int(row[1]), int(row[2]), datetime.strptime(row[3], "%d.%m.%Y")
            order = orders.pop(number, None)

            if order:   
                if number != order.number or price_usd != order.price_usd or date.strftime("%d.%m.%Y") != order.date.strftime("%d.%m.%Y"):
                    order.number = number
                    order.price_usd = price_usd
                    order.price_rub  = float(price_usd) * exchange_rate
                    order.date = date
                    order.save()
            else:
                Order.objects.create(number=number, price_usd=price_usd, price_rub=float(price_usd) * exchange_rate, date=date)
       
        # Если с вловаре остались записи, значит их не существует в таблице Google Sheet   
        if orders:
            Order.objects.filter(number__in=orders).delete()

        # задержка для не превышения лимитов по количеству запросов (60 в минуту)
        time.sleep(2)


@celeryd_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    """Запуск задачи со при запуске сервера"""
    write_sheet_data.delay() 