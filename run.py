import os
from flask import Flask, flash, redirect, render_template, request, session, url_for

import mysql.connector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
showimg_path = './static/read_from_mysql.png'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route ('/register', methods=['GET'])
def register():
    username = request.args.get("username")
    password = request.args.get("password")
    con_password = request.args.get("conpassword") 

    if not username or not password or not con_password:
        flash('Please enter your full username and password!')
        return redirect(url_for('login')) 
    if password != con_password:
        flash('The two entered passwords do not match!')
        return redirect(url_for('login'))
    
    conn = mysql.connector.connect(host="localhost",port=3306,user='root',password="yushan1022",charset="utf8",db='loobites')
    try:
        cursor = conn.cursor()
        my_query = "SELECT * FROM user where username = %s and password = %s"
        cursor.execute(my_query, (username,password))
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
            my_query = "INSERT INTO user(username,password) VALUES(%s,%s);"
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
    
    conn = mysql.connector.connect(host="localhost",port=3306,user='root',password="yushan1022",charset="utf8",db='loobites')
    try:
        cursor = conn.cursor()  
        my_query = "SELECT * FROM user where username = %s"
        cursor.execute(my_query, [username])
        res = cursor.fetchall()
    except: 
        print (1)
        flash('Login failed, reason is unknown, please contact administrator!')
        conn.rollback()
        return redirect(url_for('login'))
    
    if res:
        try:
            my_query = "SELECT * FROM user WHERE username = %s and password = %s"
            cursor.execute(my_query, [username, password])
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

        
@app.route('/index')
def index():
    return render_template('index.html',res=None, case =None)

@app.route('/restaurant_mess',methods=["GET", "POST"])
def action():
    curname = request.form.get("curname")
    curtype = request.form.get("curtype")
    curtakeout = "yes" if request.form.get("curtakeout") =="on" else "no"
    currating = request.form.get("currating")
    curprice = request.form.get("curprice")
    curremark = request.form.get("curremark")
    if request.form.get('button', '') == 'submit':
        submit(curname,curtype,curtakeout,currating,curprice,curremark)
        flash('Submission successful!')
        return redirect(url_for('index'))
    elif request.form.get('button', '') == 'reset':
        return redirect(url_for('index'))
    elif request.form.get('button','') == 'search':
        return search(curname)
    elif request.form.get('button', '') == 'match':
        return match(curname,curtype)
    else:
        flash('error')
        return render_template('index.html', res=None, case=None)
    
def search(curname):
    if not curname:
        flash('Please enter the restaurant name before searching!')
        return redirect(url_for('index'))
    
    conn = mysql.connector.connect(host="localhost",port=3306,user='root',password="yushan1022",charset="utf8",db='loobites')
    try:
        cursor = conn.cursor()  
        my_query = "SELECT * FROM restaurant_info where name = %s"
        cursor.execute(my_query,[curname])
        res = cursor.fetchall()
        cursor.close()
        conn.close()
    except: 
        flash('Search failed, reason is unknown, please contact administrator!')
        conn.rollback()
        return redirect(url_for('index'))
    
    if res:
        print(res[0])
        return render_template('index.html',res=res[0])
    else:
        flash('This restaurant doesnt exist!')
        return redirect(url_for('index'))

def submit(curname,curtype,curtakeout,currating,curprice,curremark):
    conn = mysql.connector.connect(host="localhost",port=3306,user='root',password="yushan1022",charset="utf8",db='loobites')
    try:
        cursor = conn.cursor()
        my_query = "SELECT * FROM restaurant_info where name = %s"
        cursor.execute(my_query,[curname])
        res = cursor.fetchall()
    except:
        flash('Search failed, reason is unknown, please contact administrator!')
        conn.rollback()
        return redirect(url_for('index', res=None, case=None)) 
    
    if res:
        flash("Restaurant already exists, please submit a different one!")
        cursor.close()
        conn.close()
    else:
        try:
            cursor=conn.cursor()
            my_query = "INSERT INTO restaurant_info(name,mealType,takeoutAvailable,rating,notes,priceRange) VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(my_query,[curname,curtype,curtakeout,currating,curremark,curprice])
            conn.commit()
        except:
            flash('Submission failed, error is unknown, please contact an adminstrator!')
            conn.rollback()
        cursor.close()
        conn.close()


def match(curname,curtype):
    conn = mysql.connector.connect(host="localhost",port=3306,user='root',password="yushan1022",charset="utf8",db='loobites')
    try:
        case_query = "SELECT * FROM restaurant_info where mealType = %s ORDER BY RAND() LIMIT 3"
        cursor=conn.cursor()
        cursor.execute(case_query, [curtype])
        case = cursor.fetchmany(3)
    except:
        flash('Match failed, reason is unknown, please contact administrator!')
        conn.rollback()
        return redirect(url_for('index'))
    if not case:
        flash('No such meal type in database, you should go eat more!')
    cursor.close()
    conn.close()
    print(case)
    return render_template('index.html',res=None, case=case)
        

if __name__ == '__main__':
    app.debug = True
    app.run()


