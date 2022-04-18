from datetime import datetime, timedelta
my_date = datetime.now()

today = datetime.now().date()
print(today)
# 2021-07-26 11:20:0
tomorrow = today + timedelta(days=1)
print(tomorrow)
# 2021-07-07 17:46:58.967213


# als deadline datum = date+1 (=morge)