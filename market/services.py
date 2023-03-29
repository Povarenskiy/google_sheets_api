import gspread
import requests
import xml.etree.ElementTree as ET

from google.oauth2.service_account import Credentials
from .models import ExchangeRate

from django.conf import settings


def _get_google_client():
    """Настрокйи клиента Google Api"""
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    CREDS = Credentials.from_service_account_file(settings.AUTH_JSON, scopes=SCOPE)
    return gspread.authorize(CREDS)


def _get_exchange_rate():
    """Запрос данных к ЦБ РФ  для перевода $ в рубли"""
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    root = ET.fromstring(response.text)
    rate = float(root.find("Valute[@ID='R01235']/Value").text.replace(',', '.'))

    exchange_rate, created = ExchangeRate.objects.update_or_create(exchange='usd to rub', defaults={'rate': rate})    
    return exchange_rate