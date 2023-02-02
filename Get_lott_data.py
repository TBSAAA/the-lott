import time
from datetime import datetime, timedelta, date
import random

import requests
import Connect
from send_wechat_message import send_message
from local_settings import start_date, daily_tasks


class GetLottData(object):
    def __init__(self, type):
        self.type = type
        self.url = "https://data.api.thelott.com/sales/vmax/web/data/lotto/results/search/daterange"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "content-type": "application/json",
            "accept": "*/*",
            "origin": "https://www.thelott.com",
            "referer": "https://www.thelott.com/",
        }

    def send_request(self):
        for i in range(2):
            try:
                time.sleep(random.randint(1, 5))
                res = requests.post(self.url, headers=self.headers, json=self.data)
                data_list = res.json()
                res.close()
                draw_list = []
                for data in data_list['Draws']:
                    draw_number = data['DrawNumber']
                    draw_date = data['DrawDate'].split('T')[0]
                    primary_numbers_list = data['PrimaryNumbers']
                    secondary_numbers_list = data['SecondaryNumbers']

                    primary_numbers = ",".join(str(i) for i in primary_numbers_list)
                    secondary_numbers = ",".join(str(i) for i in secondary_numbers_list)

                    draw_list.append((draw_number, draw_date, primary_numbers, secondary_numbers))

                with Connect.Connect() as conn:
                    sql = "INSERT INTO {} VALUES (%s,%s,%s,%s)".format(self.type)
                    conn.execute_many(sql, draw_list)
                return
            except Exception as e:
                sleep_time = 60
                print(e)

        # send message to wechat
        print("fail")

    def get_data(self, start):
        end = date.today()
        for i in range(0, (end - start).days, 60):
            start_date = start + timedelta(days=i)
            end_date = start + timedelta(days=i + 59)
            if end_date > end:
                end_date = end
            start_date = str(start_date)
            end_date = str(end_date)
            # after 2020-03-22 SetForLife is not available, SetForLife744 is available
            if self.type == "SetForLife744" and str(start_date) <= "2020-03-22":
                temp = "SetForLife"
            else:
                temp = self.type
            self.data = {
                "DateStart": start_date,
                "DateEnd": end_date,
                "ProductFilter": [temp],
                "CompanyFilter": ["NSWLotteries"]
            }
            print("start_date: {}, end_date: {}".format(start_date, end_date))
            self.send_request()
