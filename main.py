from datetime import datetime, timedelta
import time
# import datetime
from Get_lott_data import GetLottData
from Connect import *
from local_settings import start_date, daily_tasks

if __name__ == '__main__':
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    # # check today's day of the week
    # week = datetime.strptime(current_date, "%Y-%m-%d").weekday()
    #
    # # Get daily tasks by day of the week
    # tasks = daily_tasks[str(week + 1)]
    # for task in tasks:
    #     # Get the latest date in the database
    #     sql = "SELECT * FROM {} ORDER BY Draw_number desc limit 1".format(task)
    #     try:
    #         # update data
    #         latest_date = Connect().fetch_one(sql)['Draw_date']
    #         start_date = latest_date + timedelta(days=1)
    #         GetLottData(task).get_data(start_date, current_date)
    #     except Exception as e:
    #         # if database is empty, fill the database with data from start_date
    #         print("fill database, {}".format(task))
    #         GetLottData(task).fill()
    start = start_date['TattsLotto']
    print(current_date,type(current_date))
    print(start,type(start))