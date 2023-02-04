import Connect
import random
import local_settings


class Analyze(object):
    def __init__(self, task):
        self.task = task
        self.primary_order_list, self.secondary_order_list = self.get_data()
        print("primary_order_list: {}".format(self.primary_order_list))
        print("secondary_order_list: {}".format(self.secondary_order_list))
        print(dict(self.primary_order_list))

    def get_data(self):
        with Connect.Connect() as conn:
            sql = "select * from {} where Draw_number > {} ORDER BY Draw_number" \
                .format(self.task, local_settings.condition[self.task])
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
            return primary_order_list, secondary_order_list

    def get_random(self):
        length = local_settings.rules[self.task][0]["primary"]
        print("length: {}".format(length))


def power_ball(task):
    with Connect.Connect() as conn:
        sql = "select * from {}".format(task)
        data_list = conn.fetch_all(sql)
        analy_p_list = []
        analy_s_list = []
        item_p = {}
        item_s = {}

        for data in data_list:
            primary_number_list = data["Primary_numbers"].split(',')
            secondary_number = data["Secondary_numbers"]
            primary_number_list_size = len(primary_number_list)
            drwa_date = data["Draw_date"]
            if primary_number_list_size == 7:
                analy_p_list.append(primary_number_list)
                analy_s_list.append(secondary_number)
        # primary
        for i in analy_p_list:
            for j in i:
                if j in item_p:
                    item_p[j] += 1
                else:
                    item_p[j] = 1
        # secondary
        for i in analy_s_list:
            if i in item_s:
                item_s[i] += 1
            else:
                item_s[i] = 1

        primary_list = sorted(item_p.items(), key=lambda x: x[1], reverse=True)
        secondary_list = sorted(item_s.items(), key=lambda x: x[1], reverse=True)

        print(primary_list)
        print(secondary_list)

        finnal_primary = []

        while len(finnal_primary) < 7:
            random_number = random.randint(25, 34)
            if primary_list[random_number][0] not in finnal_primary:
                finnal_primary.append(primary_list[random_number][0])
        random_number = random.randint(17, 19)
        finnal_secondary = secondary_list[random_number][0]

        # 随机后10位+随机后3位
        print("随机后10位+随机后3位")
        print(finnal_primary)
        print(finnal_secondary)

        # 完全后7位+完全后1位
        print("完全后7位+完全后1位")
        zui_primary = []
        for i in primary_list[-7:]:
            zui_primary.append(i[0])
        print(zui_primary)
        print(secondary_list[-1][0])

        # primary（前10位随机取3，后10位随机取4）+secondary（后5位随机）
        print("primary（前10位随机取3，后10位随机取4）+secondary（后5位随机）")
        ban_primary = []
        while len(ban_primary) < 3:
            random_number = random.randint(0, 9)
            if primary_list[random_number][0] not in ban_primary:
                ban_primary.append(primary_list[random_number][0])
        while len(ban_primary) < 7:
            random_number = random.randint(25, 34)
            if primary_list[random_number][0] not in ban_primary:
                ban_primary.append(primary_list[random_number][0])
        ban_secondary = secondary_list[random.randint(15, 19)][0]
        print(ban_primary)
        print(ban_secondary)

        # 完全随机
        sui_primary = []
        print("完全随机")
        while len(sui_primary) < 7:
            random_number = random.randint(0, 34)
            if primary_list[random_number][0] not in sui_primary:
                sui_primary.append(primary_list[random_number][0])
        sui_secondary = secondary_list[random.randint(0, 19)][0]
        print(sui_primary)
        print(sui_secondary)


def set_for_life(task):
    with Connect.Connect() as conn:
        sql = "select * from {} where Draw_number > 1690".format(task)
        data_list = conn.fetch_all(sql)
        analy_p_list = []
        analy_s_list = []
        for data in data_list:
            analy_p_list.append(data["Primary_numbers"].split(','))
            analy_s_list.append(data["Secondary_numbers"].split(','))

        item_p = {}
        item_total = {}
        for i in analy_p_list:
            for j in i:
                if j in item_p:
                    item_p[j] += 1
                    item_total[j] += 1
                else:
                    item_p[j] = 1
                    item_total[j] = 1

        for i in analy_s_list:
            for j in i:
                if j in item_total:
                    item_total[j] += 1
                else:
                    item_total[j] = 1

        primary_list = sorted(item_p.items(), key=lambda x: x[1], reverse=True)
        total_list = sorted(item_total.items(), key=lambda x: x[1], reverse=True)
        print(primary_list)
        print(total_list)
        print(
            "---------------------------------------------------------------------------------------------------------")

        # 最后14位选7
        print("最后14位随机选7")
        zui_primary = []
        while len(zui_primary) < 7:
            random_number = random.randint(30, 43)
            if primary_list[random_number][0] not in zui_primary:
                zui_primary.append(primary_list[random_number][0])
        print(zui_primary)

        # 总的最后选7位
        print("总的最后选7位")
        zui_total = []
        while len(zui_total) < 7:
            random_number = random.randint(34, 43)
            if total_list[random_number][0] not in zui_total:
                zui_total.append(total_list[random_number][0])
        print(zui_total)

        # 全随机
        print("全随机")
        sui_primary = []
        while len(sui_primary) < 7:
            random_number = random.randint(0, 43)
            if total_list[random_number][0] not in sui_primary:
                sui_primary.append(total_list[random_number][0])
        print(sui_primary)


if __name__ == '__main__':
    # Analyze("SetForLife744")
    # Analyze("Powerball")
    # Analyze("TattsLotto")
    Analyze("LottoStrike")
