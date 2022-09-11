from django.db import models
from djongo import models as d_models
from .managers import HistoryManager, RawDataManager


class Consultation_history(models.Model):

    datetime = models.DateTimeField(auto_now_add=True, blank=False)
    open_price = models.FloatField("Open price", blank=False)
    high_price = models.FloatField("High price", blank=False)
    low_price = models.FloatField("Low price", blank=False)
    close_price = models.FloatField("Close price", blank=False)
    volume_btc = models.FloatField("Volume BTC", blank=False)
    volume_usd = models.FloatField("Volume USD", blank=False)
    trend_prediction = models.FloatField("Prediccion de tendencia", blank=False)

    objects = HistoryManager()

    class Meta:
        verbose_name = "consultation history"
        verbose_name_plural = "consultation history"

    def __str__(self):
        return self.id


class Raw_data(d_models.Model):

    close_time = d_models.BigIntegerField(blank=False)
    open_price = d_models.FloatField(blank=False)
    high_price = d_models.FloatField(blank=False)
    low_price = d_models.FloatField(blank=False)
    close_price = d_models.FloatField(blank=False)
    volume_BTC = d_models.FloatField(blank=False)
    volume_USD = d_models.FloatField(blank=False)

    objects = RawDataManager()

    class Meta:
        verbose_name = "Raw data"
        verbose_name_plural = "Raw data"

    def __str__(self):
        return str(self.id)
