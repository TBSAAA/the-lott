import Connect
import random
import local_settings
import base64
import pickle


class AnalyzeBetNumbers(object):
    def __init__(self, task):
        self.task = task
        self.primary_order_list, self.secondary_order_list = self.get_data()
        self.primary_length = local_settings.rules[self.task][0]["primary"]
        self.primary_list = []
        self.secondary_list = []
        # print("primary_order_list: {}".format(self.primary_order_list))
        # print("secondary_order_list: {}".format(self.secondary_order_list))
        # self.follow_stats_2()
        # print("primary_list: {}".format(self.primary_list))
        # print("secondary_list: {}".format(self.secondary_list))

    def get_data(self):
        with Connect.Connect() as conn:
            sql = "select * from AnalyzeData where name = '{}'".format(self.task)
            data = conn.fetch_one(sql)
            # decode and base64 decode
            primary_list_base64 = base64.b64decode(data["primary_order_list"].encode())
            secondary_list_base64 = base64.b64decode(data["secondary_order_list"].encode())
            # deserialized data
            primary_list = pickle.loads(primary_list_base64)
            secondary_list = pickle.loads(secondary_list_base64)
            return primary_list, secondary_list

    # totally random
    def get_random(self):
        while len(self.primary_list) < self.primary_length:
            random_number = random.randint(0, len(self.primary_order_list) - 1)
            if self.primary_order_list[random_number][0] not in self.primary_list:
                self.primary_list.append(self.primary_order_list[random_number][0])

        if self.task != "Powerball":
            return self.primary_list
        random_number = random.randint(0, len(self.secondary_order_list) - 1)
        self.secondary_list.append(self.secondary_order_list[random_number][0])
        print("primary_list: {}".format(self.primary_list))
        print("secondary_list: {}".format(self.secondary_list))
        return self.primary_list, self.secondary_list

    # follow the stats, only buy cold numbers
    def follow_stats_1(self):
        for i in range(1, self.primary_length + 1):
            self.primary_list.append(self.primary_order_list[-i][0])

        if self.task != "Powerball":
            return self.primary_list
        self.secondary_list.append(self.secondary_order_list[-1][0])
        return self.primary_list, self.secondary_list

    # follow the stats, only buy hot numbers
    def follow_stats_2(self):
        for i in range(0, self.primary_length):
            self.primary_list.append(self.primary_order_list[i][0])

        if self.task != "Powerball":
            return self.primary_list
        self.secondary_list.append(self.secondary_order_list[0][0])
        return self.primary_list, self.secondary_list

    # The first 2-6 digits take 2 digits, and the last 10 digits take the rest.
    def strategy_1(self):
        pass

    # The first half takes 2 digits, and the second half takes the rest.
    def strategy_2(self):
        pass

    # Randomly take 2 digits and then take the rest from the last 8 digits.
    def strategy_3(self):
        pass


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

        # ?????????10???+?????????3???
        print("?????????10???+?????????3???")
        print(finnal_primary)
        print(finnal_secondary)

        # ?????????7???+?????????1???
        print("?????????7???+?????????1???")
        zui_primary = []
        for i in primary_list[-7:]:
            zui_primary.append(i[0])
        print(zui_primary)
        print(secondary_list[-1][0])

        # primary??????10????????????3??????10????????????4???+secondary??????5????????????
        print("primary??????10????????????3??????10????????????4???+secondary??????5????????????")
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

        # ????????????
        sui_primary = []
        print("????????????")
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

        # ??????14??????7
        print("??????14????????????7")
        zui_primary = []
        while len(zui_primary) < 7:
            random_number = random.randint(30, 43)
            if primary_list[random_number][0] not in zui_primary:
                zui_primary.append(primary_list[random_number][0])
        print(zui_primary)

        # ???????????????7???
        print("???????????????7???")
        zui_total = []
        while len(zui_total) < 7:
            random_number = random.randint(34, 43)
            if total_list[random_number][0] not in zui_total:
                zui_total.append(total_list[random_number][0])
        print(zui_total)

        # ?????????
        print("?????????")
        sui_primary = []
        while len(sui_primary) < 7:
            random_number = random.randint(0, 43)
            if total_list[random_number][0] not in sui_primary:
                sui_primary.append(total_list[random_number][0])
        print(sui_primary)


if __name__ == '__main__':
    # Analyze("SetForLife744")
    t = AnalyzeBetNumbers("OzLotto")
    # Analyze("TattsLotto")
    # Analyze("LottoStrike")
    # primary_dict = {}
    # for i in t.primary_list:
    #     primary_dict[i[0]] = i[1]
    #     print(i[0], i[1])
    #
    # print(primary_dict)
    #

    primary_dict = dict(t.primary_order_list)
    secondary_dict = dict(t.secondary_order_list)
    print("primary_dict = ", primary_dict)
    print("secondary_dict = ", secondary_dict)

    for i in secondary_dict:
        if i in primary_dict:
            primary_dict[i] += secondary_dict[i]
        else:
            primary_dict[i] = secondary_dict[i]
    print("primary_dict = ", primary_dict)

    primary_order_list = sorted(primary_dict.items(), key=lambda x: x[1], reverse=True)
    print("primary_order_list = ", primary_order_list)

    f = []
    while len(f) < 7:
        random_number = random.randint(1, 46)
        if primary_order_list[random_number][0] not in f:
            f.append(primary_order_list[random_number][0])

    print(f)

    f2 = []
    while len(f2) < 7:
        random_number = random.randint(30, 46)
        if primary_order_list[random_number][0] not in f2:
            f2.append(primary_order_list[random_number][0])

    print(f2)

    f3 = []

    while len(f3) < 3:
        random_number = random.randint(1, 20)
        if primary_order_list[random_number][0] not in f3:
            f3.append(primary_order_list[random_number][0])

    while len(f3) < 7:
        random_number = random.randint(20, 46)
        if primary_order_list[random_number][0] not in f3:
            f3.append(primary_order_list[random_number][0])

    print(f3)

    f4 = []

    while len(f4) < 2:
        random_number = random.randint(1, 20)
        if primary_order_list[random_number][0] not in f4:
            f4.append(primary_order_list[random_number][0])

    while len(f4) < 7:
        random_number = random.randint(20, 47)
        if primary_order_list[random_number][0] not in f4:
            f4.append(primary_order_list[random_number][0])

    print(f4)