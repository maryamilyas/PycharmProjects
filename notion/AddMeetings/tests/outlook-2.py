import win32com.client, datetime
from datetime import date
from dateutil.parser import *
import calendar
import pandas as pd


Outlook = win32com.client.Dispatch('Outlook.Application')
ns = Outlook.GetNamespace('MAPI')
appts = ns.getDefaultFolder(9).Items

appts.Sort('[Start]')
appts.IncludeRecurrences = 'True'

end = date.today().strftime('%m/%d/%Y')
begin = date.today() - datetime.timedelta(days=10)
begin = begin.strftime('%m/%d/%Y')
appts = appts.Restrict('[Start] >= "' + begin + '" AND [END] <= "' + end + '"')

# Step 3, block 2 : populate dictionary of meetings
apptDict = {}
item = 0
for indx, a in enumerate(appts):
    subject = str(a.Subject)
    organizer = str(a.Organizer)
    meetingDate = str(a.Start)

    date = parse(meetingDate).date()
    duration = str(a.duration)

    apptDict[item] = {'Duration': duration, 'Organizer': organizer, 'Subject': subject,
                      'Date': date.strftime('%m/%d/%Y %H:%M')}
    item = item + 1

apt_df = pd.DataFrame.from_dict(apptDict, orient='index', columns=['Duration', 'Organizer', 'Subject', 'Date'])
apt_df = apt_df.set_index('Date')
apt_df['Meetings'] = apt_df[['Duration', 'Organizer', 'Subject']].agg(' | '.join, axis=1)
grouped_apt_df = apt_df.groupby('Date').agg({'Meetings': ', '.join})
grouped_apt_df.index = pd.to_datetime(grouped_apt_df.index)
grouped_apt_df.sort_index()

filename = date.today().strftime('%Y%m%d') + '_10day_meeting_list.csv'
grouped_apt_df.to_csv(filename, index=True, header=True)