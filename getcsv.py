import pymysql
import pandas as pd

# port = 3306,
conn = pymysql.connect(host='192.168.1.103',
    user = 'root',
    password = 'Iot2059..@',
    database = 'iot',
    charset = 'utf8')

def getrel(sql):
    cur = conn.cursor()
    ret = cur.execute(sql)
    print(f'本次查询共获得了{ret}条信息')
    col_result = cur.description
    rel = cur.fetchall()

    sql2='''REPAIR TABLE iot.device_log'''
    cur.execute(sql2)

    columns = []
    for i in range(0, len(col_result)):
        columns.append(col_result[i][0])
    print(columns)

    cur.close()
    conn.close()
    return rel,columns

def getcsv(rel,columns):
    data1 = list (map(list, rel))
    df = pd.DataFrame(data=data1,columns=columns)
    df.to_csv(path_or_buf="AAAAAA.csv",
    sep=',',
    encoding='utf-8',
    header=True,
    index=False)

if __name__ == '__main__':
    sql = 'select * from device_log order by create_time desc limit 500;'
    rel,columns = getrel(sql)
    getcsv(rel,columns)