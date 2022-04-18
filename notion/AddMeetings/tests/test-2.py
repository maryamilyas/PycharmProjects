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
today_start = date.today()
today_end = date.today() + 7
today_start = datetime.datetime.strptime(today_start, "%Y-%m-%d")
today_end = datetime.datetime.strptime(today_end, "%Y-%m-%d")

today = date.today()
start_datetime = (datetime.datetime.combine(today_start, start_time)).strftime("%Y-%m-%d %H:%M")
end_datetime = datetime.datetime.combine(today_end, end_time).strftime("%Y-%m-%d %H:%M")
