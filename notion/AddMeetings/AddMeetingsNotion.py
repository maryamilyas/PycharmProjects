from win32com.client import Dispatch
from datetime import datetime, timedelta
from notion.client import NotionClient
from datetime import date
import datetime
from notion.collection import NotionDate
from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast("Notion update", "Your script has been started to run")
token = '58c816105dcd52a5b4d2ce7cc65490ca115a999897879c5b3a038da8e5d0cfccd98ada24f44394e98d5dcf9d54d7209d7422bae283da83b92b496af92771a1fc37e47c739ff024a4dccdf50055ee'
client = NotionClient(token_v2=token)
calendar_url = 'https://www.notion.so/maryamilyas/42a936bef9224cfdbf0d366dd3b81587?v=bd4b882f0464467792d095cd09d69171'

collection_view = client.get_collection_view(calendar_url)
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
OUTLOOK_FORMAT = '%Y-%m-%d %H:%M'
outlook = Dispatch("Outlook.Application")
ns = outlook.GetNamespace("MAPI")
prev_value = ["ab", "ba"]
calcTableBody = []
start_time = datetime.time(0)
end_time = datetime.time(23)

day = date.today()
start = day - timedelta(days=day.weekday())
end = start + timedelta(days=10)
print(start)
start_datetime = (datetime.datetime.combine(start, start_time)).strftime("%Y-%m-%d %H:%M")
end_datetime = datetime.datetime.combine(end, end_time).strftime("%Y-%m-%d %H:%M")
print(start_datetime)
print(end_datetime)

appointments = ns.GetDefaultFolder(9).Items
appointments.Sort("[Start]")
appointments.IncludeRecurrences = "True"

# Step 2, block 1 : filter to the range: from = (today - 10), to = (today)

appointments = appointments.Restrict("[Start] >= '" + start_datetime + "' AND [End] <= '" + end_datetime + "'")
print(appointments)
# Iterate through restricted AppointmentItems and print them


for appointmentItem in appointments:
    print(appointmentItem)
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

print(calcTableBody)


def add_Row_by_me(rij):
    new_row = collection_view.collection.add_row()
    new_row.Name = rij[0]
    new_row.When = NotionDate(start=datetime.datetime.strptime(rij[1], "%Y-%m-%d %H:%M"),
                              end=datetime.datetime.strptime(rij[2], "%Y-%m-%d %H:%M"),
                              timezone=rij[3],
                              reminder=True
                              )
    new_row.Type = 'Daily meeting'
    new_row.Project = 'Eneco'
    new_row.URL = rij[5]
    new_row.Weekday = week_days[(datetime.datetime.strptime(rij[2], "%Y-%m-%d %H:%M")).weekday()]
    new_row.Addedby = 'Python'



def filterdate(time_list):
    print(type(start_datetime))
    print(type(end_datetime))
    today_start_1 = datetime.datetime.strftime(start, '%Y-%m-%d')
    # today_start_1 = datetime.datetime.strftime(today_start_1, '%Y-%m-%d')
    today_end_1 = datetime.datetime.strftime(end, '%Y-%m-%d')
    # today_end_1 = datetime.datetime.strftime(today_end_1, '%Y-%m-%d')

    if time_list >= today_start_1 and time_list <= today_end_1:
        return True
    else:
        return False


# def checkifexistnotion(value):
#     print(value[0])
#     for row in collection_view.collection.get_rows(search=value[0]):
#         start_datetime_2 = NotionDate.to_notion(row.When)[0][1][0][1]["start_date"] + ' ' +  NotionDate.to_notion(row.When)[0][1][0][1]["start_time"]
#         end_datetime_2 = NotionDate.to_notion(row.When)[0][1][0][1]["end_date"] + ' ' + \
#                         NotionDate.to_notion(row.When)[0][1][0][1]["end_time"]
#         if filterdate(NotionDate.to_notion(row.When)[0][1][0][1]["start_date"]):
#            if row.name == value[0].strip() and start_datetime_2 == value[1] and end_datetime_2 == value[2]:
#                return True
#     return False


i = 0
for rij in calcTableBody:
    # if not checkifexistnotion(rij):
    add_Row_by_me(rij)
    i = i + 1
notification_status = str(i) + " new row(s) added into Notion"
toaster.show_toast("Notion update", notification_status)

for c in calcTableBody:
    subject = c[0]
    if len(collection_view.collection.get_rows(search=subject)) > 1:
        for row in collection_view.collection.get_rows(search=subject):
            if row.name == prev_value[0] and NotionDate.to_notion(row.When) == prev_value[1]:
                row.remove()
            prev_value = [row.Name.strip(), NotionDate.to_notion(row.When)]

toaster.show_toast("Ready!", "Your notion is up-to-date!")
