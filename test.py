import requests
import Connect
url = "https://data.api.thelott.com/sales/vmax/web/data/lotto/results/search/drawrange"
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "content-type": "application/json",
    "accept": "*/*",
    "origin": "https://www.thelott.com",
    "referer": "https://www.thelott.com/",
}
data = {
    "MinDrawNo": 1691,
    "MaxDrawNo": 1696,
    # "Product": "Powerball", # 1 Powerball 最小期数
    # "Product": "OzLotto", # 609 OzLotto 最小期数
    # "Product": "MonWedLotto", # 1638 MonWedLotto 最小期数
    # "Product": "LottoStrike", # 1639 TattsLotto 最小期数
    # "Product": "SetForLife", # 1 LottoStrike 最小期数
    "Product": "SetForLife744",  # 1639 TattsLotto 最小期数
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
    secondary_numbers_list = data['SecondaryNumbers']

    primary_numbers = ",".join(str(i) for i in primary_numbers_list)
    secondary_numbers = ",".join(str(i) for i in secondary_numbers_list)

    draw_list.append((draw_number, draw_date, primary_numbers, secondary_numbers))

with Connect.Connect() as conn:
    sql = "INSERT INTO {} VALUES (%s,%s,%s,%s)".format("SetForLife744")
    conn.execute_many(sql, draw_list)
# print(res.text)
# draw_list = []
# for data in data_list['Draws']:
#     draw_number = data['DrawNumber']
#     draw_date = data['DrawDate'].split('T')[0]
#     primary_numbers_list = data['PrimaryNumbers']
#     power_ball_list = data['SecondaryNumbers']
#     winner_number = data["Dividends"][0]['BlocNumberOfWinners']
#     award_amount = data["Dividends"][0]['BlocDividend']
#
#     primary_numbers = ",".join(str(i) for i in primary_numbers_list)
#     power_ball = "".join(str(i) for i in power_ball_list)
#
#     draw_list.append((draw_number, draw_date, primary_numbers, power_ball, winner_number, award_amount))
#
# set_many_data("INSERT INTO lott_draw VALUES (%s,%s,%s,%s,%s,%s)", draw_list)

#
# Education = {
#     "School": "Western Sydney University",
#     "degree": "Bachelor of Computer Science",
#     "Major": ["Systems Programming", "Cyber Security"],
#     "year": "06/2019-07/2022",
# }
#
# course = ['Database Design and Development', 'Network Security', 'Mobile Applications Development',
#           'Object Oriented Programming', 'Computer Organisation', 'Operating Systems Programming',
#           'Systems Programming', 'Data Structures and Algorithms', 'Web Systems Development',
#           'Information Security', 'Distributed system programming', 'Robotic Programming',
#           'Computer Graphics']
#
# skills = {
#     "Programming": ["Python", "Java", "C", "C++", "C#", "JavaScript", "HTML", "CSS", "PHP", "SQL", "Shell"],
#     "Database": ["MySQL", "SQLite", "MongoDB", "Redis"],
# }
#
# languages = ["English", "Mandarin"]
#
# Technical_Skills = {
#     "Programming Languages": ["Python", "C", "C++", "Shell", "SQL", "JavaScript", "HTML", "CSS", "Java", "C#", "PHP"],
#     "Database": ["MySQL", "Redis"],
#     "Web Development": ["Django Framework", "Django REST framework", "Bootstrap", "jQuery", "Ajax", "JSON", "HTML5"],
#     "Software Development Methodologies": ["Agile"],
#     "Version Control": ["Git"],
#     "cloud": ["AWS"],
#     "Other": ["linux", "Nginx", "Postman", "Docker"],
# }
# Skill = ["Problem-Solving", "Teamwork", "Communication", "Language Proficiency (Mandarin, English)"]
