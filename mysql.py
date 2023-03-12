import mysql.connector

conn = mysql.connector.connect(user='root',password='yushan1022',host='localhost',database='pain',charset='utf8mb4',cursorclass=mysql.connector.cursors.Dictcursor)

cursor = conn.cursor()

sql = "select * from user"
cursor.execute(sql)
conn.commit()

data = cursor,fetchall()

print(data)