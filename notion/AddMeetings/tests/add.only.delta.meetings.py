from win32com.client import Dispatch
from datetime import timedelta
from notion.client import NotionClient
from datetime import date
import datetime
from notion.collection import NotionDate
from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast("Notion update", "Your script has been started to run")
token = 'f81b9789f45500290b02e0320b363b5ff453f927d43d4f369717579026e4b93c5ac7b6ec45dd1f5038badc45d0a18d4c5472ad205de674a1568991f6da42c9343647fefdec749943f422195464f8'
client = NotionClient(token_v2=token)
calendar_url = 'https://www.notion.so/maryamilyas/42a936bef9224cfdbf0d366dd3b81587?v=afec5328f75d40cbb93f1c1a42b1a216'

collection_view = client.get_collection_view(calendar_url)
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
OUTLOOK_FORMAT = '%Y-%m-%d %H:%M'
outlook = Dispatch("Outlook.Application")
ns = outlook.GetNamespace("MAPI")

appointments = ns.GetDefaultFolder(9).Items
appointments.Sort("[Start]")
appointments.IncludeRecurrences = "True"

# Iterate through restricted AppointmentItems and print them
prev_value = ["ab", "ba"]
calcTableBody = []

start_time = datetime.time(7)
end_time = datetime.time(23)
today_start = '2021-02-15'
today_end = '2021-02-21'
today_start = datetime.datetime.strptime(today_start, "%Y-%m-%d")
today_end = datetime.datetime.strptime(today_end, "%Y-%m-%d")

# today = date.today()
start_datetime = (datetime.datetime.combine(today_start, start_time)).strftime("%Y-%m-%d %H:%M")
end_datetime = datetime.datetime.combine(today_end, end_time).strftime("%Y-%m-%d %H:%M")

for appointmentItem in appointments:
    if (appointmentItem.Start.Format(OUTLOOK_FORMAT) > start_datetime) & (
            appointmentItem.Start.Format(OUTLOOK_FORMAT) < end_datetime):
        row = []
        row.append(appointmentItem.Subject)
        row.append(appointmentItem.Start.Format(OUTLOOK_FORMAT))
        row.append((appointmentItem.Start + timedelta(minutes=appointmentItem.Duration)).Format(OUTLOOK_FORMAT))
        row.append('Central European Time (UTC+01:00)')
        row.append({'unit': 'minute', 'value': 30})
        row.append(appointmentItem.body)
        calcTableBody.append(row)


def add_Row_by_me(rij):
    new_row = collection_view.collection.add_row()
    new_row.Name = rij[0]
    new_row.When = NotionDate(start=datetime.datetime.strptime(rij[1], "%Y-%m-%d %H:%M"),
                              end=datetime.datetime.strptime(rij[2], "%Y-%m-%d %H:%M"),
                              timezone=rij[3])
    new_row.Type = 'Daily meeting'
    new_row.Project = 'RTL'
    new_row.URL = rij[5]
    new_row.Weekday = week_days[(datetime.datetime.strptime(rij[2], "%Y-%m-%d %H:%M")).weekday()]
    new_row.Addedby = 'Python'


def filterdate(time_list):
    today_start_1 = datetime.datetime.strftime(today_start, '%Y-%m-%d')
    today_end_1 = datetime.datetime.strftime(today_end, '%Y-%m-%d')
    if time_list >= today_start_1 and time_list <= today_end_1:
        return True
    else:
        return False


def checkifexistnotion(value):
    for row in collection_view.collection.get_rows(search=value[0]):
        print(type(NotionDate.to_notion(row.When)[0][1][0][1]["start_time"]))
        start_datetime_2 = NotionDate.to_notion(row.When)[0][1][0][1]["start_date"] + ' ' + \
                           NotionDate.to_notion(row.When)[0][1][0][1]["start_time"]
        end_datetime_2 = NotionDate.to_notion(row.When)[0][1][0][1]["end_date"] + ' ' + \
                         NotionDate.to_notion(row.When)[0][1][0][1]["end_time"]
        if filterdate(NotionDate.to_notion(row.When)[0][1][0][1]["start_date"]):
            if row.name == value[0].strip() and start_datetime_2 == value[1] and end_datetime_2 == value[2]:
                return True
    return False


i = 0
for rij in calcTableBody:
    if not checkifexistnotion(rij):
        add_Row_by_me(rij)
        i = i + 1
notification_status = str(i) + " new row(s) added into Notion"
toaster.show_toast("Notion update", notification_status)

for c in calcTableBody:
    subject = c[0]
    if len(collection_view.collection.get_rows(search=subject)) > 1:
        for row in collection_view.collection.get_rows(search=subject):
            if row.name == prev_value[0] and NotionDate.to_notion(row.When) == prev_value[1]:
                print("Duplicate value deleted")
                row.remove()
            prev_value = [row.Name.strip(), NotionDate.to_notion(row.When)]

toaster.show_toast("Ready!", "Your notion is up-to-date!")
