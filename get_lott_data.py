import time
import random

import requests
from connect_mysql import *
from send_wechat_message import send_message


def get_lott(start, end):
    url = "https://data.api.thelott.com/sales/vmax/web/data/lotto/results/search/drawrange"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "accept": "*/*",
        "origin": "https://www.thelott.com",
        "referer": "https://www.thelott.com/",
    }
    data = {
        "MinDrawNo": start,
        "MaxDrawNo": end,
        "Product": "Powerball",
        "CompanyFilter": ["NSWLotteries"]
    }

    res = requests.post(url, headers=headers, json=data)
    data_list = res.json()
    res.close()
    draw_list = []
    for data in data_list['Draws']:
        draw_number = data['DrawNumber']
        draw_date = data['DrawDate'].split('T')[0]
        primary_numbers_list = data['PrimaryNumbers']
        power_ball_list = data['SecondaryNumbers']
        winner_number = data["Dividends"][0]['BlocNumberOfWinners']
        award_amount = data["Dividends"][0]['BlocDividend']

        primary_numbers = ",".join(str(i) for i in primary_numbers_list)
        power_ball = "".join(str(i) for i in power_ball_list)

        draw_list.append((draw_number, draw_date, primary_numbers, power_ball, winner_number, award_amount))

    set_many_data("INSERT INTO lott_draw VALUES (%s,%s,%s,%s,%s,%s)",draw_list)


def run(s, e):
    for i in range(s, e, 50):
        start = i
        end = start + 49
        if end > e:
            end = e
        get_lott(start, end)
        time.sleep(random.randint(4, 8))


if __name__ == "__main__":
    start = 1
    end = 1392
    run(start, end)
    send_message(3, 1, "所有lott数据已经更新完毕")

