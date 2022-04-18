import requests, json
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

token = 'secret_hDfCxLw3HCThHylR22iBOErC73r20LE1Lkxjehegej4'
databaseId = '10b1302b7a9a4f1ca390cc8b57c3f0d6'
page_id = 'fd76a19448604ca6a08aeccf688a739f'
headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2021-05-13"
}
pd.set_option("display.max_rows", None, "display.max_columns", None)

connection = psycopg2.connect(user="postgres",
                              password="Maryam1793",
                              host="127.0.0.1",
                              port="5432",
                              database="postgres")
cursor = connection.cursor()

conn_string = 'postgresql://postgres:Maryam1793@localhost:5432/postgres'


# https://api.notion.com/v1/pages/fd76a19448604ca6a08aeccf688a739f

def ReadMetaData(databaseId, headers):
    calcTableBody = []
    columns = ['year', 'quarter', 'tabletype', 'title', 'databaseid']
    ReadPageUrl = f"https://api.notion.com/v1/blocks/{page_id}/children"
    ReadPage = requests.request("GET", ReadPageUrl, headers=headers)
    ReadPage = ReadPage.json()
    for y in ReadPage['results']:
        if y['type'] == "toggle":
            year = y['toggle']['text'][0]['text']['content']
            OpenYearToggleUrl = f"https://api.notion.com/v1/blocks/{y['id']}/children"
            ReadYearToggle = requests.request("GET", OpenYearToggleUrl, headers=headers)
            ReadYearToggle = ReadYearToggle.json()
            for q in ReadYearToggle['results']:
                if q['type'] == "toggle":
                    Quarter = q['toggle']['text'][0]['text']['content']
                    OpenQuarterToggleUrl = f"https://api.notion.com/v1/blocks/{q['id']}/children"
                    ReadQuarterToggle = requests.request("GET", OpenQuarterToggleUrl, headers=headers)
                    ReadQuarterToggle = ReadQuarterToggle.json()
                    for tt in ReadQuarterToggle['results']:
                        TableType = tt['toggle']['text'][0]['text']['content'][: - 5]
                        OpenTableTypeToggleUrl = f"https://api.notion.com/v1/blocks/{tt['id']}/children"
                        ReadTableTypeToggle = requests.request("GET", OpenTableTypeToggleUrl, headers=headers)
                        ReadTableTypeToggle = ReadTableTypeToggle.json()
                        if ReadTableTypeToggle['results'][0]['type'] == 'child_database':
                            list = []
                            list.append(year)
                            list.append(Quarter)
                            list.append(TableType)
                            list.append(ReadTableTypeToggle['results'][0]['child_database']['title'])
                            list.append(ReadTableTypeToggle['results'][0]['id'])
                            calcTableBody.append(list)
    df = pd.DataFrame(calcTableBody, columns=columns)
    return df

    # readUrl = f"https://api.notion.com/v1/databases/{databaseId}"
    # res = requests.request("GET", readUrl, headers=headers)
    # json_string = res.json()
    # columns = ['DatabaseID', 'DatabaseName', 'CreatedTime', 'LastUpdatedTime']
    # listDatabase = []
    # listDatabase.append(json_string['id'])
    # listDatabase.append(json_string['title'][0]['plain_text'])
    # listDatabase.append(json_string['created_time'])
    # listDatabase.append(json_string['last_edited_time'])
    # # df = pd.DataFrame(listDatabase, columns=columns)
    # # print(df)
    # return listDatabase


#
def ReadExpenses(databaseId, headers):
    calcTableBody = []
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    # data = res.json()
    # print(res.status_code)
    # print(type(res))
    json_string = res.json()
    # print(json_string)
    columns = ['expenseid', 'parentdatabaseid', 'desciption', 'date', 'amount', 'budgetcategoryid']
    for expense in json_string['results']:
        row = []
        row.append(expense['id'])
        row.append(expense['parent']['database_id'])
        row.append(expense['properties']['Expenses']['title'][0]['plain_text'])
        row.append(expense['properties']['Date']['date']['start'])
        row.append(expense['properties']['Amount']['number'])
        row.append(expense['properties']['Budget Category']['relation'][0]['id'])
        calcTableBody.append(row)
    df = pd.DataFrame(calcTableBody, columns=columns)
    return df

def ReadIncome(databaseId, headers):
    calcTableBody = []
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"
    res = requests.request("POST", readUrl, headers=headers)
    json_string = res.json()
    # print(json_string)
    columns = ['incomeid', 'parentdatabaseid', 'description', 'date', 'amount',
               'RelationToFinalOverview', 'JanRefundRelation', 'FebRefundRelation', 'MarRefundRelation',
               'AprRefundRelation', 'MayRefundRelation', 'JunRefundRelation', 'JulRefundRelation',
               'AugRefundRelation', 'SepRefundRelation', 'OktRefundRelation', 'NovRefundRelation', 'DecRefundRelation']
    for income in json_string['results']:
        row = []
        row.append(income['id'])
        row.append(income['parent']['database_id'])
        row.append(income['properties']['Name']['title'][0]['text']['content'])
        row.append(income['created_time'])
        # row.append(income['properties']['Date']['date']['start'])
        row.append(income['properties']['Amount']['number'])
        # row.append(income['properties']['Category']['select']['name'])
        if not len(income['properties']['Related to Final Overview']['relation']) == 0 :
            row.append(income['properties']['Related to Final Overview']['relation'][0]['id'])
        else:
            row.append('')
        Properties = income['properties']
        if "Jan_refund_relation" in Properties:
            row.append(income['properties']['Jan_refund_relation']['relation'])
            row.append(income['properties']['Feb_refund_relation']['relation'])
            row.append(income['properties']['Mar_refund_relation']['relation'])
            row.append(income['properties']['Apr_refund_relation']['relation'])
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append('')
        elif "May_refund_relation" in Properties:
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append(income['properties']['May_refund_relation']['relation'])
            row.append(income['properties']['Jun_refund_relation']['relation'])
            row.append(income['properties']['Jul_refund_relation']['relation'])
            row.append(income['properties']['Aug_refund_relation']['relation'])
            row.append('')
            row.append('')
            row.append('')
            row.append('')
        elif "Sep_refund_relation" in Properties:
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append('')
            row.append(income['properties']['Sep_refund_relation']['relation'])
            row.append(income['properties']['Okt_refund_relation']['relation'])
            row.append(income['properties']['Nov_refund_relation']['relation'])
            row.append(income['properties']['Dec_refund_relation']['relation'])
        calcTableBody.append(row)
    df = pd.DataFrame(calcTableBody, columns=columns)
    return df

def ReadMonthlyBudget(databaseId, headers):
    calcTableBody = []
    print(databaseId)
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"
    res = requests.request("POST", readUrl, headers=headers)
    json_string = res.json()
    columns = ['expenseid', 'parentdatabaseid', 'desciption', 'date', 'amount', 'budgetcategoryid']
    for expense in json_string['results']:
        row = []
        row.append(expense['id'])
        row.append(expense['parent']['database_id'])
        row.append(expense['created_time'])
        row.append(expense['properties']['Name']['title'][0]['plain_text'])
        row.append(expense['properties']['Budget_pocket']['formula']['number'])
        row.append(expense['properties']['Org_budget']['number'])
        row.append(expense['properties']['Total expense']['rollup']['number'])
        row.append(expense['properties']['Opnemen in Savings?']['checkbox'])
        Q1 = ['Jan', 'Feb', 'Mar', 'Apr']
        Q2 = ['May', 'Jun', 'Jul', 'Aug']
        Q3 = ['Sep', 'Okt', 'Nov', 'Dec']
        Quarters = [Q1, Q2, Q3]

        for Quart in Quarters:
            for Q in Quart:
                row.append(expense['properties']['{Q}_budget']['formula']['number'])
                row.append(expense['properties']['{Q}_expenses']['formula']['number'])
                row.append(expense['properties']['{Q}_refund']['rollup']['string'])
                row.append(expense['properties']['{Q}_extra_saving']['formula']['number'])
                row.append(expense['properties']['{Q}_eind_rapport']['formula']['string'])
                row.append(expense['properties']['{Q}_exp_org']['number'])

        # row.append(expense['properties']['Okt_budget']['formula']['number'])
        # row.append(expense['properties']['Okt_expenses']['formula']['number'])
        # row.append(expense['properties']['Okt_refund']['rollup']['number'])
        # row.append(expense['properties']['Okt_extra_saving']['formula']['number'])
        # row.append(expense['properties']['Okt_eind_rapport']['formula']['string'])
        # row.append(expense['properties']['Okt_exp_org']['number'])
        #
        #
        # row.append(expense['properties']['Nov_budget']['formula']['number'])
        # row.append(expense['properties']['Nov_expenses']['formula']['number'])
        # row.append(expense['properties']['Nov_refund']['rollup']['number'])
        # row.append(expense['properties']['Nov_extra_saving']['formula']['number'])
        # row.append(expense['properties']['Nov_eind_rapport']['formula']['string'])
        # row.append(expense['properties']['Nov_exp_org']['number'])
        #
        # row.append(expense['properties']['Dec_budget']['formula']['number'])
        # row.append(expense['properties']['Dec_expenses']['formula']['number'])
        # row.append(expense['properties']['Dec_refund']['rollup']['array'])
        # row.append(expense['properties']['Dec_extra_saving']['formula']['number'])
        # row.append(expense['properties']['Dec_eind_rapport']['formula']['string'])
        # row.append(expense['properties']['Dec_exp_org']['formula']['number'])

        calcTableBody.append(row)
    df = pd.DataFrame(calcTableBody, columns=columns)
    return df


MetaData = ReadMetaData(databaseId, headers)
# print(MetaData.loc[0][0])
#
# for i in range(len(MetaData)):
#     postgres_insert_query = """ INSERT INTO budget.metadata (year, quarter, table_type, title, database_id) VALUES (%s,%s,%s,%s,%s)"""
#     record_to_insert = (MetaData.loc[i, 'year'],
#                         MetaData.loc[i, 'quarter'],
#                         MetaData.loc[i, 'tabletype'],
#                         MetaData.loc[i, 'title'],
#                         MetaData.loc[i, 'databaseid'])
#     cursor.execute(postgres_insert_query, record_to_insert)
#     connection.commit()
#
db = create_engine(conn_string)
conn = db.connect()
for i in range(len(MetaData)):
    if MetaData.loc[i, 'tabletype'] == "Expense log":
        # Expenses = ReadExpenses(MetaData.loc[i, 'databaseid'], headers)
        # Expenses.to_sql('expenselog', con=conn, if_exists='replace', index=False)
        print('it is an expense log')
    if MetaData.loc[i, 'tabletype'] == "Income log":
        # Income = ReadIncome(MetaData.loc[i, 'databaseid'], headers)
        # Income.to_sql('incomelog', con=conn, if_exists='replace', index=False)
        print('it is an income log')
    if MetaData.loc[i, 'tabletype'] == "Monthly budget":
        Income = ReadMonthlyBudget(MetaData.loc[i, 'databaseid'], headers)
        # Income.to_sql('incomelog', con=conn, if_exists='replace', index=False)

#
# budget.to_sql('expenselog', con=conn, if_exists='replace', index=False)
#
conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()
conn.close()

# try:
#     connection = psycopg2.connect(user="sysadmin",
#                                   password="Maryam1793",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="postgres_db")
#     cursor = connection.cursor()
#
#     postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
#     record_to_insert = (5, 'One Plus 6', 950)
#     cursor.execute(postgres_insert_query, record_to_insert)
#
#     connection.commit()
#     count = cursor.rowcount
#     print(count, "Record inserted successfully into mobile table")
