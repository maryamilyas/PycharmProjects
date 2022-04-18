from notion.client import NotionClient
from datetime import datetime

from notion.collection import NotionDate

token = 'f81b9789f45500290b02e0320b363b5ff453f927d43d4f369717579026e4b93c5ac7b6ec45dd1f5038badc45d0a18d4c5472ad205de674a1568991f6da42c9343647fefdec749943f422195464f8'

client = NotionClient(token_v2=token)
calendar_url = 'https://www.notion.so/maryamilyas/42a936bef9224cfdbf0d366dd3b81587?v=afec5328f75d40cbb93f1c1a42b1a216'
collection_view = client.get_collection_view(calendar_url)

new_row = collection_view.collection.add_row()
today = datetime.today()
start = datetime.strptime("2020-01-01 09:30", "%Y-%m-%d %H:%M")
end = datetime.strptime("2020-01-01 10:30", "%Y-%m-%d %H:%M")
timezone = "Central European Time (UTC+01:00)"
reminder = {'unit': 'minute', 'value': 30}

new_row.Name = 'Continue ETL activities2'
new_row.When = NotionDate(start, end=end, timezone=timezone)
new_row.Type = 'Daily meeting'
new_row.Project = 'RTL'
