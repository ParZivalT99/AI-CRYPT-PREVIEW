import json
from datetime import datetime, date, timedelta
from dateutil import tz

from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy

# models
from .models import (
    Consultation_history,
    Raw_data,
)

# own functions
from data_test.MLdata import (
    MLData as prediction,
)

# Mixins
class ConvertAndFormatDatetimeMixin(object):
    def convert_utc_to_local_time(
        self, datetime_to_convert: datetime, formart: bool = True
    ):

        datetime_to_convert = datetime_to_convert.replace(tzinfo=tz.tzutc())

        current_timezone = timezone.localtime().tzinfo
        current_datetime = datetime_to_convert.astimezone(current_timezone)

        if formart:
            current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            current_datetime = datetime.strptime(current_datetime, "%Y-%m-%d %H:%M:%S")

        return current_datetime


class CandlestickDataMixin(ConvertAndFormatDatetimeMixin, object):
    def last_month_data(self):

        current_data = Consultation_history.objects.last()
        queryset = Raw_data.objects.order_by("-close_time")[:31]

        current_year = str(date.today().year)
        data = []

        append_none = lambda data_list: data_list.append(
            {
                "x": "None",
                "y": "None",
            }
        )

        for i in queryset:
            i.close_time = str(
                self.convert_utc_to_local_time(datetime.fromtimestamp(i.close_time))
            )

            if i.close_time[:4] == current_year:
                data.append(
                    {
                        "x": i.close_time,
                        "y": [i.open_price, i.high_price, i.low_price, i.close_price],
                    }
                )

        data = list(reversed(data))

        if current_data is None:
            append_none(data)

        else:
            last_date = datetime.strptime(data[-1]["x"], "%Y-%m-%d %H:%M:%S")
            last_consult = self.convert_utc_to_local_time(current_data.datetime)

            if last_date >= last_consult:
                append_none(data)

            else:
                if last_consult.date() == last_date.date():
                    last_consult = last_consult + timedelta(days=1)

                last_consult = last_consult.replace(hour=19, minute=0, second=0)

                data.append(
                    {
                        "x": str(last_consult),
                        "y": [
                            current_data.open_price,
                            current_data.high_price,
                            current_data.low_price,
                            current_data.close_price,
                        ],
                    }
                )

        return data


class InicioView(TemplateView):
    template_name = "dashboard_app/inicio.html"


class PredictionView(CandlestickDataMixin, TemplateView):
    template_name = "dashboard_app/prediction_full.html"

    def get(self, request, *args, **kwargs):
        if request.META.get("HTTP_HX_REQUEST"):
            # with access
            return reverse_lazy("dashboard_app:prediction-consult")

        # no access
        return super(PredictionView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Consultation_history.objects.last()
        return queryset

    def get_context_data(self, **kwargs):

        context = super(PredictionView, self).get_context_data(**kwargs)

        to_json = lambda x: json.dumps(x)

        consult = self.get_queryset()

        if consult:

            candlestick_data = to_json(self.last_month_data())

            context = {
                "datetime": consult.datetime,
                "OpenPrice": consult.open_price,
                "ClosePrice": consult.close_price,
                "HighPrice": consult.high_price,
                "LowPrice": consult.low_price,
                "prediction_value": float(consult.trend_prediction),
                "VolumeUSD": consult.volume_usd,
                "VolumeBTC": consult.volume_btc,
                "accuracy": 100,
                "candlestick_data": candlestick_data,
            }
        else:
            context = {
                "datetime": "None",
                "OpenPrice": 0,
                "ClosePrice": 0,
                "HighPrice": 0,
                "LowPrice": 0,
                "prend_prediction": 0,
                "VolumeUSD": 0,
                "VolumeBTC": 0,
                "accuracy": 0,
            }

        return context


class PredictionConsultView(CandlestickDataMixin, TemplateView):
    template_name = "dashboard_app/prediction_short.html"

    def __load_prediction(self):
        pred = prediction()
        pred = pred.get_prediction()
        return pred

    def __save_consult(self):

        consult = self.__load_prediction()
        consult = consult[0]

        Consultation_history.objects.add_consult(
            consult["OpenPrice"],
            consult["HighPrice"],
            consult["LowPrice"],
            consult["ClosePrice"],
            consult["VolumeBTC"],
            consult["VolumeUSD"],
            consult["prediction_value"],
        )
        return consult

    def get_queryset(self):
        last_consult = Consultation_history.objects.last()

        return last_consult

    def get_context_data(self, **kwargs):

        context = super(PredictionConsultView, self).get_context_data(**kwargs)

        consult = self.__save_consult()  # saving consult of prediction

        context = context | consult  # dictionary merge: between context and consult

        to_json = lambda x: json.dumps(x)
        candlestick_data = to_json(self.last_month_data())

        last_consult = self.get_queryset()

        print(timezone.localtime())
        context["datetime"] = last_consult.datetime
        context["accuracy"] = 100
        context["candlestick_data"] = candlestick_data

        return context


class HistoryPredictionView(ConvertAndFormatDatetimeMixin, ListView):
    template_name = "dashboard_app/history.html"
    paginate_by = 2
    model = Consultation_history
    context_object_name = "history"

    def get_context_data(self, **kwargs):

        context = super(HistoryPredictionView, self).get_context_data(**kwargs)

        queryset = self.get_queryset()
        all_predictions, all_datetime = self.datetime_consult(queryset)

        page = self.request.GET.get("page")
        query = self.request.GET.get("p")

        if queryset:
            if query != None:

                id = query

                consult = [i for i in queryset.filter(id=id)]

                consult[0].trend_prediction = float(
                    format(float(consult[0].trend_prediction), ".2f")
                )

                context["datetime"] = consult[0].datetime
                context["open_price"] = consult[0].open_price
                context["high_price"] = consult[0].high_price
                context["low_price"] = consult[0].low_price
                context["close_price"] = consult[0].close_price
                context["volume_btc"] = consult[0].volume_btc
                context["volume_usd"] = consult[0].volume_usd
                context["trend_prediction"] = consult[0].trend_prediction
                context["accuracy"] = 100
                context["all_consults"] = all_predictions
                context["all_datetime"] = all_datetime
                context["page"] = page
                context["query"] = query

            else:

                consult = queryset.last()

                consult.trend_prediction = float(
                    format(float(consult.trend_prediction), ".2f")
                )

                context["datetime"] = consult.datetime
                context["open_price"] = consult.open_price
                context["high_price"] = consult.high_price
                context["low_price"] = consult.low_price
                context["close_price"] = consult.close_price
                context["volume_btc"] = consult.volume_btc
                context["volume_usd"] = consult.volume_usd
                context["trend_prediction"] = consult.trend_prediction
                context["accuracy"] = 100
                context["all_consults"] = all_predictions
                context["all_datetime"] = all_datetime
                context["page"] = page
                context["query"] = query
        else:
            context["datetime"] = "None"
            context["open_price"] = 0
            context["high_price"] = 0
            context["low_price"] = 0
            context["close_price"] = 0
            context["volume_btc"] = 0
            context["volume_usd"] = 0
            context["trend_prediction"] = 0
            context["accuracy"] = 0
            context["all_consults"] = 0
            context["all_datetime"] = 0
            context["page"] = 0
            context["query"] = 0

        return context

    def get_queryset(self):
        queryset = Consultation_history.objects.all().order_by("id")
        return queryset

    # return date and prediction of each consultation
    def datetime_consult(self, queryset):

        predictions = []
        all_datetime = []

        if not queryset:
            return predictions, all_datetime

        else:
            for i in queryset:
                i.trend_prediction = float(format(float(i.trend_prediction), ".3f"))
                predictions.append(float(i.trend_prediction))
                all_datetime.append(i.datetime)

            all_datetime = sorted(
                [str(self.convert_utc_to_local_time(dt)) for dt in all_datetime]
            )

            to_json = lambda x: json.dumps(x)
            predictions = to_json(predictions)
            all_datetime = to_json(all_datetime)

            return predictions, all_datetime


class TermsAndUsesView(TemplateView):
    template_name = "dashboard_app/terms_uses.html"
