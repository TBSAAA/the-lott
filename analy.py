import Connect
import random

with Connect.Connect() as conn:
    sql = "select * from power_ball"
    data_list = conn.fetch_all(sql)
    analy_p_list = []
    analy_s_list = []
    item_p = {}
    item_s = {}
    for data in data_list:
        primary_number_list = data["Primary_number"].split(',')
        secondary_number = data["Power_ball"]
        primary_number_list_size = len(primary_number_list)
        drwa_date = data["Draw_date"]
        if primary_number_list_size == 7:
            analy_p_list.append(primary_number_list)
            analy_s_list.append(secondary_number)
    for i in analy_p_list:
        for j in i:
            if j in item_p:
                item_p[j] += 1
            else:
                item_p[j] = 1

    for i in analy_s_list:
        if i in item_s:
            item_s[i] += 1
        else:
            item_s[i] = 1

    print(sorted(item_p.items(), key=lambda x: x[1], reverse=True))
    print(sorted(item_s.items(), key=lambda x: x[1], reverse=True))


    # print(item_p)