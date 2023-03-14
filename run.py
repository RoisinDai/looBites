from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route ('/register', methods=['GET'])
def register():
    username = request.args.get("username")
    print(username)
    password = request.args.get("password")
    print(password) 
    con_password = request.args.get("conpassword") 

    if not username or not password or not con_password:
        flash('Please enter your full username and password!')
        return redirect(url_for('login')) 
    if password != con_password:
        flash('The two entered passwords do not match!')
        return redirect(url_for('login'))
    
    conn = mysql.connector.connect(host="local host",port=3306,user='root',password="yushan1022",charset="utf8",db='users')
    try:
        cursor = conn.cursor(cursor=mysql.connector.cursors.DictCursor)
        my_query = "SELECT * FROM user where usr = %s and password = %s"
        cursor.execute(my_query, [username,password])
        conn.commit()

        res = cursor.fetchall()
    except:
        flash('Failed to register new user, reason is unknown, please contact administrator!')
        conn.rollback()
        return redirect(url_for('login'))

    if res:
        cursor.close()
        conn.close()
        flash('This user already exists! Please login, or re-enter your username!')
        return redirect(url_for('login'))
    else:
        try:
            my_query = "INSERT INTO user(usr,password) VALUES(%s,%s);"
            cursor.execute(my_query, (username,password))
            conn.commit()
            flash('New user has been registered, please proceed to login!"')
        except: 
            flash('Failed to register new user, reason is unknown, please contact administrator!')
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('login')) 

@app.route('/loginer',methods=['GET'])
def loginer():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        flash('Please enter your full username and password! ')
        return redirect(url_for('login'))
    
    conn = mysql.connector.connect(host="local host",port=3306,user='root',password="yushan1022",charset="utf8",db='users')
    try:
        cursor = conn.cursor(cursor=mysql.connector.cursors.DictCursor)  
        my_query = "SELECT * FROM user where usr = %s"
        cursor.execute(my_query, [username])
        conn.commit()

        res = cursor.fetchall()
    except: 
        flash('Login failed, reason is unknown, please contact administrator!')
        conn.rollback()
        return redirect(url_for('login'))
    
    if res:
        try:
            my_query = "SELECT * FROM user WHERE usr = %s and password = %s"
            cursor.execute(my_query, [username, password])
            conn.commit()
            res = cursor.fetchall()
            cursor.close()
            conn.close
            if res: 
                session['login_success'] = 'permission'
                return redirect(url_for('index'))
            else:
                flash('Password is wrong, please retry')
                return redirect(url_for('login'))
        except: 
            flash('Login failed, reason is unknown, please contact administrator!')
            conn.rollback()
            return redirect(url_for('login'))
    else:
        cursor.close()
        conn.close()
        flash('This username does not exist, please register!')
        return redirect(url_for('login'))

        

@app.route('/')
def index():
    permission = session.get('login_success')
    if not permission:
        return redirect(url_for('login'))
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()



import mysql.connector

conn = mysql.connector.connect(user='root',password='yushan1022',host='localhost',database='users',charset='utf8mb4',cursorclass=mysql.connector.cursors.Dictcursor)

cursor = conn.cursor()

sql = "select * from user"
cursor.execute(sql)
conn.commit()

data = cursor,fetchall()

print(data)

