# Send tasks that are due tomorrow.
# Task name: Daily tasks
# This script is run everyday in the nigh on 20:15.
from win10toast import ToastNotifier

import requests, json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

import pywhatkit
from datetime import date

toaster = ToastNotifier()
toaster.show_toast("Notion update", "Your script has been started to run")


today = datetime.now().date()
tomorrow = today + timedelta(days=1)

pd.set_option('display.max_columns', None)
pd.options.display.width = None

token = 'secret_hDfCxLw3HCThHylR22iBOErC73r20LE1Lkxjehegej4'
databaseId = '6420c115ec874b66a1f6a13616d1d5a9'
headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2021-05-13"
}

def MultiSelectList(expense, column):
    selec = []
    for selects in expense['properties'][column]['multi_select']:
        selec.append(selects['name'])
    return selec

def ReadDatabase(databaseId, headers):
    calcTableBody = []
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    json_string = res.json()
    print(json_string)
    columns = ['Id', 'Name', 'Notes', 'Deadline', 'Type', 'CreatedAt', 'Status', 'TaskFor']

    for expense in json_string['results']:
        row = []
        # Id
        row.append(expense['id'])
        # Name
        if expense['properties']['Name']['title']:
            row.append(expense['properties']['Name']['title'][0]['plain_text'])
        else:
            row.append("No name")
        # Notes
        if expense['properties']['Notes']['rich_text']:
            row.append(expense['properties']['Notes']['rich_text'][0]['plain_text'])
        else:
            row.append("No notes")
        # Deadline
        date = '9999-01-01T00:00:00.000+02:00'
        if 'Deadline' in expense['properties']:
            date = expense['properties']['Deadline']['date']['start']
        if len(date) > 10:
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            date = datetime.strptime(date, '%Y-%m-%d')

        row.append(date)

        # Type
        row.append(MultiSelectList(expense, 'Type'))
        # CreatedTime
        if expense['properties']['Create at']['created_time']:
            row.append(expense['properties']['Create at']['created_time'])
        # Status
        if 'Status' in expense['properties']:
            row.append(expense['properties']['Status']['select']['name'])
        else:
            row.append('No status')
        # TaskFor
        row.append(MultiSelectList(expense, 'For'))
        calcTableBody.append(row)
    df = pd.DataFrame(calcTableBody, columns=columns)
    return df


PhoneNumbers = {"Maryam": '+32484348696',
                "Nida": '+32465905724',
                "Sana": '+32494428226',
                "Papa": '+923334507593',
                "Mama": '+32465219289',
                "Ahmed": '+32465775588'}

Results = ReadDatabase(databaseId, headers)
print(Results)
print(type(Results))
test = '+32497076834'
for row in Results.values:
    if row[3].date() == tomorrow and row[6] != 'Completed':
        if row[7]:
            for name in row[7]:
                if name != 'Maryam':
                    now = datetime.now()
                    hour = now.hour
                    now = now + timedelta(minutes=1)
                    minute = now.minute
                    if row[4]:
                        for type in row[4]:
                            if type == 'Appointment':
                                pywhatkit.sendwhatmsg(PhoneNumbers[name],
                                                      'Apki kal appointment hai: ' + row[
                                                          1] + ' is time py ' + str(row[3]) + ' - ' + row[2]
                                                      , hour, minute)
                            else:
                                pywhatkit.sendwhatmsg(PhoneNumbers[name],
                                                      'Kal tak apnay yeh kaam khtum kerna hai: ' + row[1] + ' - ' + row[2]
                                                      , hour, minute)
                            break

# Tasks that are completed
