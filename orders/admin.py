from django.contrib import admin

from .models import Rate, Currency, Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order_number', 'usd_price', 'shipment_date',
                    'rub_price', 'is_deleted',)
    search_fields = ('pk', 'order_number', 'usd_price', 'shipment_date',
                     'rub_price', 'is_deleted',)
    empty_value_display = '-empty-'


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'iso_code', 'iso_title',)
    search_fields = ('pk', 'title', 'iso_code', 'iso_title',)
    empty_value_display = '-empty-'


class RateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'currency', 'rate', 'nominal', 'date',)
    search_fields = ('pk', 'currency__title', 'rate', 'nominal', 'date',)
    empty_value_display = '-empty-'


admin.site.register(Order, OrderAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Rate, RateAdmin)
