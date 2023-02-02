from datetime import datetime, timedelta
import time
# import datetime
from Get_lott_data import GetLottData
import Connect
from local_settings import start_date, daily_tasks
from get_latest_date import get_latest

if __name__ == '__main__':
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    # check today's day of the week
    week = datetime.strptime(current_date, "%Y-%m-%d").weekday()

    # Get daily tasks by day of the week
    tasks = daily_tasks[str(week + 1)]
    for task in tasks:
        # update data
        with Connect.Connect() as conn:
            # Get the latest date in the database
            sql = "SELECT * FROM {} ORDER BY Draw_number desc limit 1".format(task)
            date = conn.fetch_one(sql)
        if date:
            latest_date = date["Draw_date"]
            print("latest_date: {}".format(latest_date))
            print("get_latest: {}".format(get_latest(task)))
            if str(latest_date) == get_latest(task):
                print("no need to update, {}".format(task))
                continue
            start = latest_date + timedelta(days=1)
            GetLottData(task).get_data(start)
        else:
            # if database is empty, fill the database with data from start_date
            print("fill database, {}".format(task))
            start = datetime.strptime(start_date[task], '%Y-%m-%d').date()
            GetLottData(task).get_data(start)


