from datetime import datetime, timedelta
import time



start_date = {
    "Powerball": "1996-05-23",
    "OzLotto": "2005-10-18",
    "MonWedLotto": "1997-12-28",
    "LottoStrike": "1997-12-31",
    "SetForLife744": "2020-03-20",
    "TattsLotto": "2024-02-01",
}


start = datetime.strptime(start_date["SetForLife744"], '%Y-%m-%d').date()
print(start)
if str(start) <= "2020-03-22":
    print("SetForLife")
else:
    print("SetForLife744")
