from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route ('/register', methods=['GET'])
def register():
    username = request.args.get("username") 
    password = request.args.get("password") 
    con_password = request.args.get("con_password") 

    if not username or not password or not con_password:
        #note
        return redirect(url_for('login')) 
    if password != con_password:
        #note
        return redirect(url_for('login'))
    
    conn = mysql.connector.connect(host="local host",port=3306,user='root',password="yushan1022",charset="utf8",db='restaurants')
    try:
        cursor = conn.cursor(cursor=mysql.connector.cursors.DictCursor)
        my_query = "SELECT * FROM user where usr = %s and password = %s"
        cursor.execute(my_query, [username],password)
        conn.commit()

        res = cursor.fetchall()
    except:
        conn.rollback()

    if res:
        cursor.close()
        conn.close()
        #note
        return redirect(url_for('login'))
    else:
        try:
            my_query = "INSERT INTO user(usr,password) VALUES(%s,%s)"
            cursor.execute(my_query, (username,password))
            conn.commit()
            #note
        except: 
            #note
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('login')) 



@app.route('/')
def mainPage():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()



import mysql.connector

conn = mysql.connector.connect(user='root',password='yushan1022',host='localhost',database='restaurants',charset='utf8mb4',cursorclass=mysql.connector.cursors.Dictcursor)

cursor = conn.cursor()

sql = "select * from user"
cursor.execute(sql)
conn.commit()

data = cursor,fetchall()

print(data)

