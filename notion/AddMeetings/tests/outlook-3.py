from win32com.client import Dispatch
from datetime import date
from tabulate import tabulate
from datetime import timedelta
import datetime
from notion.client import NotionClient
from datetime import datetime
from notion.collection import NotionDate
import pdb

OUTLOOK_FORMAT = '%m/%d/%Y %H:%M'
outlook = Dispatch("Outlook.Application")
ns = outlook.GetNamespace("MAPI")

appointments = ns.GetDefaultFolder(9).Items 

# Restrict to items in the next 30 days (using Python 3.3 - might be slightly different for 2.7)
#begin = datetime.date.today()
#end = begin + datetime.timedelta(days=10)

end = date.today().strftime('%m/%d/%Y')
begin = (date.today()+ timedelta(days=0)).strftime('%m/%d/%Y')
# begin1 = date.today() - timedelta(days=0)
# begin = begin1.strftime('%m/%d/%Y')

restriction = '[Start] >= "' + begin + '" AND [END] <= "' + end + '"'
restrictedItems = appointments.Restrict(restriction)
appointments.Sort("[Start]")
appointments.IncludeRecurrences = "FALSE"

# Iterate through restricted AppointmentItems and print them
calcTableHeader = ['Title', 'Organizer', 'Start', 'Duration(Minutes)','End']
calcTableBody = []

for appointmentItem in appointments:
    row=[]
    row.append(appointmentItem.Subject)
    row.append(appointmentItem.Organizer)
    row.append(appointmentItem.Start.Format(OUTLOOK_FORMAT))
    row.append(appointmentItem.Duration)
    row.append((appointmentItem.Start + timedelta(minutes=appointmentItem.Duration)).Format(OUTLOOK_FORMAT))
    calcTableBody.append(row)

# file_name = "meeting-extract"
# open_file=open(file_name,"wb")

filtered = []
for row in calcTableBody:
    # if row[0] == 'Onderonsje':

    if (row[2]>'01/28/2021 01:00') & (row[2]<'01/28/2021 23:00'):
        filtered.append(row[0])
        filtered.append(row[1])
        filtered.append(row[2])
        filtered.append(row[3])


print(filtered)
# print(tabulate(calcTableBody, headers=calcTableHeader))

