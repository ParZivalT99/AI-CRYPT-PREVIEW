import json
import requests
import time
import pandas as pd
import random

from applications.dashboard_app.models import Raw_data


class MLData:
    def __init__(self):
        try:
            with open("secret.json") as s:
                self.api_url = json.loads(s.read())["API_CONECTION_URL"]
        except Exception as e:
            raise e

    def get_btc_raw_data(self, current_raw_data: bool = False):

        """
        current_raw_data: bool, default False
            if True returns the current BTC raw data, otherwise returns all historical BTC raw data.

        return: DataFrame
        """

        url = self.api_url
        period = "86400"
        params = {"periods": period}

        try:
            if current_raw_data:
                current_time = int(time.time())
                params["after"] = current_time

            else:
                last_data = Raw_data.objects.last()

                if last_data:
                    params["after"] = last_data.close_time

            response = requests.get(url, params=params)

            if response.status_code != 200:
                raise Exception("Something has gone wrong with the request")

            data = response.json()

            df = pd.DataFrame(
                data["result"][period],
                columns=[
                    "CloseTime",
                    "OpenPrice",
                    "HighPrice",
                    "LowPrice",
                    "ClosePrice",
                    "VolumeBTC",
                    "VolumeUSD",
                ],
            )

        except Exception as e:
            raise e

        return df

    def data_clean(self, df: pd.DataFrame, current_raw_data: bool = False):

        """
        df: DataFrame.
        current_raw_data: bool, default False
        return: List
        """

        # removing rows with zero values from the given columns and restoring their index
        index_zero = df[(df.T == 0).any()].index

        df.drop(index=index_zero, inplace=True)

        df = df.reset_index().drop(["index"], axis=1)

        # dataFrame to list dict
        dic = list(json.loads(df.T.to_json()).values())

        if current_raw_data is False:
            if Raw_data.objects.last():

                queryset = Raw_data.objects.filter(
                    close_time__in=[t["CloseTime"] for t in dic],
                ).values("close_time")

                queryset = [i["close_time"] for i in queryset]

                no_duplicate = []
                if not queryset:
                    return dic

                else:
                    for i in dic:
                        if i["CloseTime"] not in queryset:
                            no_duplicate.append(i)

                    return no_duplicate
            else:
                return dic
        else:
            return dic

    def insert_data(self):
        """
        Method that inserts all historical btc data into the database.
        """
        df = self.get_btc_raw_data(False)
        df = self.data_clean(df, False)

        if df:
            Raw_data.objects.add_raw_data(df)
            print("Successful insert!")
        else:
            print("There is no new data!")

    def get_prediction(self):
        """
        Method that returns a fictitious prediction of the btc trend.
        """
        df = self.get_btc_raw_data(True)
        df = self.data_clean(df, True)
        df[0]["prediction_value"] = self.random_prediction()

        return df

    def random_prediction(self):
        return round(random.uniform(-10.0, 10.0), 2)


