import pymysql
import pandas as pd

# port = 3306,
conn = pymysql.connect(host='192.168.1.103',
    user = 'root',
    password = 'Iot2059..@',
    database = 'iot',
    charset = 'utf8')

cur = conn.cursor()
print(cur)

cur.execute("select version()")
result = cur.fetchone()
print("test: %s" % result)

sql2='''REPAIR TABLE iot.device_log'''
cur.execute(sql2)

sql1= '''select * from device_log order by create_time desc limit 500;'''
ret = cur.execute(sql1)
print(f'本次查询共获得了{ret}条信息')

df = pd.read_sql(sql1,conn)
df.to_csv(
    path_or_buf="test.csv",
    sep='\t',
    encoding='utf-8',
    header=False,
    index=False)
cur.close()