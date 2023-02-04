import time
from datetime import datetime, timedelta, date
import random

import requests
import Connect
import local_settings


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

    def update_analyze_data(self):
        with Connect.Connect() as conn:
            sql = "select * from {} where Draw_number > {} ORDER BY Draw_number" \
                .format(self.type, local_settings.condition[self.type])
            data_list = conn.fetch_all(sql)
            primary_list = []
            secondary_list = []
            for data in data_list:
                primary_list.append(data["Primary_numbers"].split(','))
                secondary_list.append(data["Secondary_numbers"].split(','))
            primary_temp_list = {}
            secondary_temp_list = {}

            for i in primary_list:
                for j in i:
                    if j in primary_temp_list:
                        primary_temp_list[j] += 1
                    else:
                        primary_temp_list[j] = 1

            for i in secondary_list:
                for j in i:
                    if j in secondary_temp_list:
                        secondary_temp_list[j] += 1
                    else:
                        secondary_temp_list[j] = 1

            primary_order_list = sorted(primary_temp_list.items(), key=lambda x: x[1], reverse=True)
            secondary_order_list = sorted(secondary_temp_list.items(), key=lambda x: x[1], reverse=True)

            # sql = "UPDATE AnalyzeData SET primary_order_list = {}, secondary_order_list = {} WHERE name = {}".format(
            #     1, 2, self.type)
            sql = "UPDATE AnalyzeData SET primary_order_list = {}, secondary_order_list = {}".format(
                primary_order_list, secondary_order_list)
            print(sql)
            # primary_order_list: [('22', 210), ('1', 208), ('5', 201), ('11', 199), ('7', 199), ('40', 197), ('39', 196),
            #                      ('24', 196), ('18', 196), ('12', 194), ('42', 194), ('6', 191), ('32', 189),
            #                      ('16', 188), ('38', 188), ('33', 188), ('26', 187), ('21', 187), ('25', 184),
            #                      ('37', 184), ('8', 183), ('41', 182), ('3', 181), ('15', 180), ('10', 180),
            #                      ('31', 180), ('23', 179), ('27', 178), ('36', 178), ('17', 178), ('34', 177),
            #                      ('29', 176), ('20', 176), ('19', 176), ('45', 175), ('13', 172), ('9', 171),
            #                      ('30', 168), ('43', 161), ('4', 160), ('35', 158), ('28', 158), ('2', 154),
            #                      ('14', 144), ('44', 141)]
            # secondary_order_list: [('2', 73), ('6', 73), ('4', 71), ('11', 70), ('15', 70), ('23', 68), ('33', 66),
            #                        ('36', 66), ('8', 65), ('28', 65), ('35', 64), ('14', 64), ('41', 63), ('10', 63),
            #                        ('34', 63), ('1', 63), ('22', 62), ('38', 62), ('43', 61), ('9', 61), ('32', 61),
            #                        ('7', 61), ('26', 60), ('29', 60), ('13', 59), ('16', 59), ('5', 59), ('40', 58),
            #                        ('17', 58), ('21', 57), ('18', 57), ('20', 57), ('45', 56), ('44', 55), ('42', 55),
            #                        ('27', 55), ('24', 54), ('25', 54), ('30', 54), ('19', 53), ('12', 53), ('37', 53),
            #                        ('39', 53), ('3', 52), ('31', 48)]

            conn.execute(sql)

            # primary_order_list: [('39', 358), ('24', 355), ('42', 353), ('20', 353), ('13', 350), ('11', 349),
            #                      ('10', 345), ('22', 341), ('41', 340), ('38', 337), ('21', 336), ('17', 335),
            #                      ('23', 334), ('29', 332), ('6', 331), ('1', 329), ('32', 328), ('7', 324), ('2', 323),
            #                      ('4', 321), ('31', 320), ('14', 319), ('40', 315), ('16', 315), ('35', 315),
            #                      ('44', 314), ('12', 313), ('30', 311), ('8', 309), ('18', 309), ('3', 308),
            #                      ('34', 308), ('19', 306), ('9', 305), ('5', 305), ('36', 303), ('43', 303),
            #                      ('26', 302), ('25', 302), ('33', 301), ('28', 300), ('27', 297), ('37', 290),
            #                      ('15', 280), ('45', 272)]

if __name__ == '__main__':
    GetLottData("TattsLotto").update_analyze_data()



