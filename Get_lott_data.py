import time
import datetime
import random

import requests
from Connect import *
from send_wechat_message import send_message
from local_settings import start_date, daily_tasks


class GetLottData(object):
    def __init__(self, type):
        self.type = type
        self.url = "https://data.api.thelott.com/sales/vmax/web/data/lotto/results/search/drawrange"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "content-type": "application/json",
            "accept": "*/*",
            "origin": "https://www.thelott.com",
            "referer": "https://www.thelott.com/",
        }

    def send_request(self):
        time.sleep(random.randint(5, 10))
        res = requests.post(self.url, headers=self.headers, json=self.data)
        data_list = res.json()
        res.close()
        draw_list = []
        for data in data_list['Draws']:
            draw_number = data['DrawNumber']
            draw_date = data['DrawDate'].split('T')[0]
            primary_numbers_list = data['PrimaryNumbers']
            secondary_numbers_list = data['SecondaryNumbers']
            winner_number = data["Dividends"][0]['BlocNumberOfWinners']
            award_amount = data["Dividends"][0]['BlocDividend']

            primary_numbers = ",".join(str(i) for i in primary_numbers_list)
            secondary_numbers = ",".join(str(i) for i in secondary_numbers_list)

            draw_list.append((draw_number, draw_date, primary_numbers, secondary_numbers, winner_number, award_amount))

        sql = "INSERT INTO {} VALUES (%s,%s,%s,%s,%s,%s)".format(self.type)
        Connect().execute_many(sql, draw_list)

    def get_data(self, start):
        end = time.strftime("%Y-%m-%d", time.localtime())
        # if self.type == "TattsLotto":
        for i in range(0, (end - start).days, 60):
            start_date = start + datetime.timedelta(days=i)
            end_date = start + datetime.timedelta(days=i + 59)
            if end_date > end:
                end_date = end
            self.data = {
                "DateStart": start_date,
                "DateEnd": end_date,
                "ProductFilter": [self.type],
                "CompanyFilter": ["NSWLotteries"]
            }
            self.send_request()

        # else:
        #     for i in range(start, end_dr, 50):
        #         start_draw = i
        #         end_draw = start_draw + 49
        #         if end_draw > end_dr:
        #             end_draw = end_dr
        #
        #         self.data = {
        #             "MinDrawNo": start_draw,
        #             "MaxDrawNo": end_draw,
        #             "Product": self.type,
        #             "CompanyFilter": ["NSWLotteries"]
        #         }
        #         self.send_request()

    # def get_latest(self):
    #     url = "https://data.api.thelott.com/sales/vmax/web/data/lotto/latestresults"
    #     data = {
    #         "CompanyId": "NSWLotteries",
    #         'MaxDrawCountPerProduct': '1',
    #         "OptionalProductFilter": [self.type]
    #     }
    #     res = requests.post(url, headers=self.headers, json=data)
    #     data_list = res.json()
    #     res.close()
    #     return data_list['DrawResults'][0]['DrawDate'].split('T')[0]

    def fill(self):
        start = start_date[self.type]
        # end_date = self.get_latest()
        end_date = time.strftime("%Y-%m-%d", time.localtime())
        self.get_data(start)
