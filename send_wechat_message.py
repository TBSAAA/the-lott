import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests

from connect_mysql import *
from local_settings import Wechat


def get_access_token():
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?"
    params = {
        "corpid": Wechat["corpid"],
        "corpsecret": Wechat["corpsecret"],
    }
    res = requests.get(url, params=params)
    access_token = res.json()['access_token']
    print("get access_token")
    return access_token


def send_message(loop_num, info_level, content):
    if loop_num == 0:
        return
    if info_level == 1:
        touser = "HuangHaoRan"
    elif info_level == 2:
        touser = "HuangHaoRan|xiaoSusie"
    access_token = get_data("SELECT access_token FROM wechat_token where id=1")[0][0]
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
    data = {
        "touser": touser,
        "msgtype": "text",
        "agentid": 1000002,
        "text": {
            "content": content
        },
    }
    res = requests.post(url, json=data)
    if res.json()['errcode'] != 0:
        print('access_token expired')
        access_token = get_access_token()
        update_data("UPDATE wechat_token SET access_token='{}' where id=1".format(access_token))
        send_message(loop_num - 1, info_level, content)


if __name__ == '__main__':
    send_message(3, 2, "test message")
