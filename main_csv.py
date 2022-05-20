# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import pymysql as mysql
import pandas as pd
import datetime
import cryptography

pd.set_option('display.width', 2000)
pd.set_option('display.max_columns', None)

# con = mysql.connect(host="127.0.0.1", port=3306, user="root", passwd="Knight9z", db="new_schema", charset="utf8mb4")
#
# print("连接成功")
#
# sql = "select * from apetradedata order by trade_timestamp"
# result = pd.read_sql(sql, con=con)

result = pd.read_csv("apetradedata.csv")

result["trade_timestamp"] = pd.to_datetime(result["trade_timestamp"])

div = int(input("Time segment: "))

temp = pd.DataFrame(data=None, columns=['trade_timestamp', 'trade_unit_price', 'trade_amt'])
now_time = datetime.time()
df = pd.DataFrame([], columns=['start_timestamp', 'open_price', 'high_price', 'low_price', 'close_price', 'trade_amt'])

for index, row in result.iterrows():
    if len(temp) == 0:
        temp.loc[0] = [row['trade_timestamp'], row['trade_unit_price'], row['trade_amt']]
        dt = row['trade_timestamp']
        td = datetime.timedelta(days=0, seconds=0, microseconds=dt.microsecond, milliseconds=0, minutes=0,
                                hours=0, weeks=0)
        now_time = dt - td
    elif (row['trade_timestamp'] - now_time).total_seconds() < div:
        temp.loc[len(temp)] = [row['trade_timestamp'], row['trade_unit_price'], row['trade_amt']]
    else:
        out_arr = [now_time, temp['trade_unit_price'][0], temp['trade_unit_price'].max(),
                   temp['trade_unit_price'].min(), temp['trade_unit_price'][len(temp)-1], temp['trade_amt'].sum(axis=0)]
        df.loc[len(df)] = out_arr
        temp = temp.drop(index=temp.index)

print(df)

