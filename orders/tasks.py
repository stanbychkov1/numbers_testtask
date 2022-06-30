import decimal
from decimal import Decimal

import requests
from celery.schedules import crontab

from numbers_testtask.celery import app
import datetime
from django.core.exceptions import ValidationError

from orders import models, telegram_bot
from orders.services import oauth, ruble_calculation, create_rates

URL = 'https://www.cbr-xml-daily.ru'
HEADERS = {'User-Agent': 'Mozilla/5.0'}


@app.on_after_finalize.connect
def schedule_periodic_tasks(sender, **kwargs):
    """
        Создание расписания выполнения всех задач для Celery
    """
    # Запуск получения курса валют при запуске
    sender.send_task('get_rates')
    sender.send_task('update_rub_prices')
    sender.send_task('undelivered_orders')

    # Создание расписания для запуска задачи по получению курса валют
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        get_rates.s(),
    )

    # Создание расписания для запуска задачи по обновлению данных таблицы
    sender.add_periodic_task(30.0, get_sheet_data.s())

    # Создание расписания для запуска задачи по обновлению сумм заказов в руб.
    sender.add_periodic_task(
        crontab(hour=0, minute=1),
        update_rub_prices.s(),
    )

    # Создание расписания для запуска задачи по отправке невыполненных заказов
    # в телеграм бот
    sender.add_periodic_task(43200, undelivered_orders.s())


@app.task(bind=True, name='get_sheet_data')
def get_sheet_data(self):
    """
        Функция, которая получает данные из
        Google Sheet API, преобразовывает их в модели и сохраняет в базу.
    """
    result = oauth()
    values = result.get('values', [])

    error_list = ()
    order_list = ()

    # Обработка строк таблицы для создания и обновления моделей Заказ
    for count, value in enumerate(values[1:]):
        try:

            # Попытка найти заказ, если он уже существует в базе
            try:
                order = models.Order.objects.get(
                    order_number=value[1],
                )
            except models.Order.DoesNotExist:
                order = None

            date = datetime.datetime.strptime(value[3], '%d.%m.%Y')

            # Обработка заказа: обновления модели, создание модели
            if order:
                order_list += (order.id,)
                if order.usd_price != Decimal(value[2]):
                    order.usd_price = value[2]
                    order.rub_price = ruble_calculation(value[2])
                order.shipment_date = date
                order.is_deleted = False
                order.save()
            else:
                rub_price = ruble_calculation(value[2])
                models.Order.objects.create(
                    order_number=value[1],
                    usd_price=value[2],
                    shipment_date=datetime.datetime.date(date),
                    rub_price=rub_price
                )

        # Обработка ошибок
        except ValueError:
            response = {'error': f'Ошибка формата в строке {value[0]}'}
            error_list += (response,)
            pass

        except ValidationError:
            response = {'error': f'Ошибка формата в строке {value[0]}'}
            error_list += (response,)
            pass

        except IndexError:
            response = {'error': f'Пустая или не до конца заполненная'
                                 f' строка {count}'}
            error_list += (response,)
            pass

        except decimal.InvalidOperation:
            response = {'error': f'Ошибка формата в столбце "сумма в долларах"'
                                 f' в строке {value[0]}'}
            error_list += (response,)
            pass

    # Отмечание в БД, что заказы удалены
    deleted_orders = models.Order.objects.exclude(pk__in=order_list)
    deleted_orders.update(is_deleted=True)

    return error_list


@app.task(bind=True, name='get_rates')
def get_rates(self):
    """
        Функция, которая получает курсы валют и добавляет их в базу.
    """

    today = datetime.date.today()
    url = (f'{URL}/archive/{today.year}/{today.month:02d}/'
           f'{today.day:02d}/daily_json.js')

    # Получения курсов валют на сегодня от API CBR XML RU
    response = requests.get(url=url, headers=HEADERS)

    # Обработка ответа в соответствии со статусом ответа от сервера
    if response.status_code == 200:
        create_rates(response, today)
    elif response.status_code == 404:
        url = f'{URL}/daily_json.js'
        response = requests.get(url=url, headers=HEADERS)
        create_rates(response, today)
    else:
        pass


@app.task(bind=True, name='update_rub_prices')
def update_rub_prices(self):

    orders = models.Order.objects.exclude(is_deleted=True)

    for order in orders:
        new_rub_price = ruble_calculation(order.usd_price)
        order.rub_price = new_rub_price
        order.save()


@app.task(bind=True, name='undelivered_orders')
def undelivered_orders(self):
    today = datetime.date.today()
    orders = models.Order.objects.filter(
        shipment_date__lt=today
    )
    for order in orders:
        telegram_bot.send_message(order)
