import os
from decimal import Decimal

from google.oauth2 import service_account
from googleapiclient.discovery import build

from . import models


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    os.getenv('SERVICE_ACCOUNT_FILE'))
SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
SPREADSHEET_SIZE = os.getenv('SPREADSHEET_SIZE')


def oauth():
    """
        Авторизация и получение таблицы от GOOGLE SHEET API
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SPREADSHEET_SIZE).execute()

    return result


def ruble_calculation(usd_price):
    """
        Калькуляция стоимости в рублях от стоимость в долларах
    """
    usd_rate = models.Rate.objects.latest().rate
    usd_nominal = models.Rate.objects.latest().nominal
    return Decimal(usd_price) * (usd_rate / Decimal(usd_nominal))


def create_rates(response, date):
    """
        Добавление ежеденевных курсов валют в БД.
    """
    rates = response.json()
    usd_rate = rates['Valute']['USD']
    currency, created = models.Currency.objects.get_or_create(
        title=usd_rate['CharCode'],
        iso_title=usd_rate['CharCode'],
        iso_code=usd_rate['NumCode']
    )
    rate, created = models.Rate.objects.get_or_create(
        currency=currency,
        rate=usd_rate['Value'],
        nominal=usd_rate['Nominal'],
        date=date
    )



