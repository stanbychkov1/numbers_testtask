from django.db import models


class Order(models.Model):
    order_number = models.IntegerField(verbose_name='Номер заказа',
                                       unique=True)
    usd_price = models.DecimalField(verbose_name='Стоимость в USD',
                                    decimal_places=2,
                                    max_digits=20)
    shipment_date = models.DateField(verbose_name='Срок Поставки')
    rub_price = models.DecimalField(verbose_name='Стоимость в руб.',
                                    decimal_places=2,
                                    max_digits=20)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-shipment_date',)

    def __str__(self):
        return f'Заказ №{self.order_number} на сумму {self.usd_price} USD'


class Currency(models.Model):
    title = models.CharField(max_length=3,
                             verbose_name='Название валюты')
    iso_code = models.CharField(max_length=3,
                                unique=True,
                                verbose_name='Код ISO')
    iso_title = models.CharField(max_length=3,
                                 unique=True,
                                 verbose_name='Название ISO')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюта'

    def __str__(self):
        return f'{self.title}'


class Rate(models.Model):
    currency = models.ForeignKey(to=Currency,
                                 related_name='rate',
                                 on_delete=models.CASCADE)
    rate = models.DecimalField(decimal_places=4,
                               max_digits=20,
                               verbose_name='Курс валюты')
    nominal = models.IntegerField(verbose_name='Номинал валюты')
    date = models.DateField(db_index=True,
                            unique=True,
                            verbose_name='Дата курса')

    class Meta:
        get_latest_by = ('-date',)
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'

    def __str__(self):
        return (f'Курс валюты {self.currency} на {self.date}',
                f' составляет {self.rate}')
