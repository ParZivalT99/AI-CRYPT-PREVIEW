from django.db import models


class HistoryManager(models.Manager):
    def __add_consult(
        self,
        open_price,
        high_price,
        low_price,
        close_price,
        volume_btc,
        volume_usd,
        trend_prediction,
    ):
        history = self.model(
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            close_price=close_price,
            volume_btc=volume_btc,
            volume_usd=volume_usd,
            trend_prediction=trend_prediction,
        )
        history.save(using=self.db)
        return history

    # metodo para crear registro de un historial
    def add_consult(
        self,
        open_price,
        high_price,
        low_price,
        close_price,
        volume_btc,
        volume_usd,
        trend_prediction,
    ):

        return self.__add_consult(
            open_price,
            high_price,
            low_price,
            close_price,
            volume_btc,
            volume_usd,
            trend_prediction,
        )


class RawDataManager(models.Manager):
    def __add_raw_data(self, listDictionary):
        objs = [
            self.model(
                close_time=i["CloseTime"],
                open_price=i["OpenPrice"],
                high_price=i["HighPrice"],
                low_price=i["LowPrice"],
                close_price=i["ClosePrice"],
                volume_BTC=i["VolumeBTC"],
                volume_USD=i["VolumeUSD"],
            )
            for i in listDictionary
        ]
        # raw_data.save(using=self.db)
        self.bulk_create(objs)

        return self.model()

    # metodo para crear registro de un historial
    def add_raw_data(self, listDictionary):
        return self.__add_raw_data(listDictionary)
