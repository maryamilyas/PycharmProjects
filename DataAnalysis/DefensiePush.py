import pandas as pd
MIG4 = pd.read_excel (r'C:\Users\maryam.ilyas\Desktop\DefensiePushed.xlsx', sheet_name='MIG4')
MIG6 = pd.read_excel (r'C:\Users\maryam.ilyas\Desktop\DefensiePushed.xlsx', sheet_name='MIG6')
pd.set_option('display.max_columns', None)

print(MIG4.groupby('EANCode').count())
print(MIG6.groupby('EANCode').count())
