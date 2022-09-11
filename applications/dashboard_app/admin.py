from django.contrib import admin
from .models import Consultation_history, Raw_data


class History(admin.ModelAdmin):
    list_display = (
        "id",
        "datetime",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume_btc",
        "volume_usd",
        "trend_prediction",
    )
    search_fields = ("id",)


class Rawdata(admin.ModelAdmin):
    list_display = (
        "id",
        "close_time",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume_BTC",
        "volume_USD",
    )
    search_fields = ("id",)


admin.site.register(Consultation_history, History)
admin.site.register(Raw_data, Rawdata)
