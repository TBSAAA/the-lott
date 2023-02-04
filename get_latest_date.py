import requests


def get_latest(type):
    url = "https://data.api.thelott.com/sales/vmax/web/data/lotto/latestresults"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "accept": "*/*",
        "origin": "https://www.thelott.com",
        "referer": "https://www.thelott.com/",
    }
    data = {
        "CompanyId": "NSWLotteries",
        'MaxDrawCountPerProduct': '3',
        "OptionalProductFilter": [type]
    }

    res = requests.post(url, headers=headers, json=data)
    data_list = res.json()
    res.close()
    return data_list['DrawResults'][0]['DrawDate'].split('T')[0]


if __name__ == '__main__':
    # get_latest("OzLotto")
    print(get_latest("TattsLotto"))