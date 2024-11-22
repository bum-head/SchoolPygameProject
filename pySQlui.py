import mysql.connector as sql

from prettytable import from_db_cursor as tbl

db = sql.connect(
    host="localhost",
    user="root",
    passwd="mysqlroot2343"
    )

cursor = db.cursor()
cursor.execute("SHOW databases")

data = cursor.fetchall()
li = []
for i in data:
    li.append(i)

print(li)

b = int(input("select database: "))
v = li[b][0]
print(v)

st = f"use `{v}`"
cursor.execute(st) 


cursor.execute("show tables")
table_data = cursor.fetchall()
li2 = []
for i in table_data:
    print(i)
    li2.append(i)
st2 = int(input("select table: "))
n = li2[st2][0]
print(n)
u = int(input(": "))

gt = f"SELECT * FROM `{n}` WHERE comp_id = {u}"
cursor.execute(gt)
mytable = tbl(cursor)
print(mytable)
o = cursor.fetchall()
'''header = ["1","2","3","4","5","6"]
print(tbl(o,headers = header, tablefmt ="fancy grid"))
'''
db.close()