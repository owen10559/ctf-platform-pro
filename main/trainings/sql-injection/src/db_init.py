import pymysql
import time

# 确保mysql准备完成
for i in range(10):
    try:
        cursor = pymysql.connect(host="mysql", user="root", passwd="").cursor()
    except Exception as e:
        print(str(e))
        time.sleep(5)

cursor.execute("create database db;")
cursor = pymysql.connect(host="mysql", user="root", passwd="", db="db").cursor()
cursor.execute("create table fl4g(username varchar(32), password varchar(32));")
cursor.execute("insert into fl4g values('rooot', 'fake flag');")
cursor.execute("insert into fl4g values('root', 'flag{sql-injection}');")
cursor.connection.commit()
cursor.close()
