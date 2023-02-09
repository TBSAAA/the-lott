# readis setting
REDIS_PARAMS = {
    "host": '127.0.0.1',
    "port": "6379",
    "password": '123123',
}

# mysql setting
MYSQL_CONN_PARAMS = {
    'host': "127.0.0.1",
    'port': 3306,
    'user': 'root',
    'passwd': "123123",
    'database': "lott",
}

# Wechat params
Wechat = {
    "corpid": "",
    "corpsecret": "",
    "touser-1": "",
    "touser-2": "",
}

start_date = {
    "Powerball": "1996-05-23",
    "OzLotto": "2005-10-18",
    "MonWedLotto": "1997-12-28",
    "LottoStrike": "1997-12-31",
    "SetForLife744": "2015-08-07",
    "TattsLotto": "1997-02-01",
}

# after 2020-03-22 SetForLife is not available, SetForLife744 is available
daily_tasks = {
    "1": ["MonWedLotto", "LottoStrike", "SetForLife744"],
    "2": ["OzLotto", "SetForLife744"],
    "3": ["MonWedLotto", "LottoStrike", "SetForLife744"],
    "4": ["Powerball", "SetForLife744"],
    "5": ["SetForLife744"],
    "6": ["TattsLotto", "LottoStrike", "SetForLife744"],
    "7": ["SetForLife744"],
}

# Database query conditions
condition = {
    "Powerball": "1143",
    "OzLotto": "1",
    "MonWedLotto": "1638",
    "LottoStrike": "1638",
    "SetForLife744": "1690",
    "TattsLotto": "1620",

}

# lott number selection rules
rules = {
    "Powerball": [{"primary": 7, "secondary": 1}],
    "OzLotto": [{"primary": 7, "secondary": 0}],
    "MonWedLotto": [{"primary": 6, "secondary": 0}],
    "LottoStrike": [{"primary": 4, "secondary": 0}],
    "SetForLife744": [{"primary": 7, "secondary": 0}],
    "TattsLotto": [{"primary": 6, "secondary": 0}],
}

