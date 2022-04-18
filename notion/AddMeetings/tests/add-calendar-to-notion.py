from win32com.client import Dispatch
from datetime import datetime
from datetime import date
from tabulate import tabulate
from datetime import timedelta
from notion.client import NotionClient
from notion.collection import NotionDate

token = 'f81b9789f45500290b02e0320b363b5ff453f927d43d4f369717579026e4b93c5ac7b6ec45dd1f5038badc45d0a18d4c5472ad205de674a1568991f6da42c9343647fefdec749943f422195464f8'

client = NotionClient(token_v2=token)
calendar_url = 'https://www.notion.so/maryamilyas/42a936bef9224cfdbf0d366dd3b81587?v=afec5328f75d40cbb93f1c1a42b1a216'
collection_view = client.get_collection_view(calendar_url)

OUTLOOK_FORMAT = '%Y-%m-%d %H:%M'
outlook = Dispatch("Outlook.Application")
ns = outlook.GetNamespace("MAPI")

appointments = ns.GetDefaultFolder(9).Items

# end = date.today().strftime('%m/%d/%Y')
# begin = date.today() - timedelta(days=10)
# begin = begin.strftime('%m/%d/%Y')
#
# restriction = '[Start] >= "' + begin + '" AND [END] <= "' + end + '"'
# restrictedItems = appointments.Restrict(restriction)
appointments.Sort("[Start]")
appointments.IncludeRecurrences = "True"

# Iterate through restricted AppointmentItems and print them
calcTableHeader = ['Title', 'Start', 'End', 'Timezone','Reminder']
calcTableBody = []
for appointmentItem in appointments:
    if (appointmentItem.Start.Format(OUTLOOK_FORMAT) > '2021-01-28 01:00') & (appointmentItem.Start.Format(OUTLOOK_FORMAT) < '2021-01-28 23:00'):
        row = []
        row.append(appointmentItem.Subject)
        row.append(appointmentItem.Start.Format(OUTLOOK_FORMAT))
        row.append((appointmentItem.Start + timedelta(minutes=appointmentItem.Duration)).Format(OUTLOOK_FORMAT))
        row.append('Central European Time (UTC+01:00)')
        row.append({'unit': 'minute', 'value': 30})
        calcTableBody.append(row)


for rij in calcTableBody:
    new_row = collection_view.collection.add_row()
    new_row.Name = rij[0]
    new_row.When = NotionDate(start=datetime.strptime(rij[1], "%Y-%m-%d %H:%M"), end=datetime.strptime(rij[2], "%Y-%m-%d %H:%M"),
                          timezone=rij[3])
    new_row.Type = 'Daily meeting'
    new_row.Project = 'Python'
    new_row.Weekday = week_days[(datetime.datetime.strptime(rij[2], "%Y-%m-%d %H:%M")).weekday()]