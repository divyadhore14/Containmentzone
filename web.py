from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import requests
from flask_bootstrap import Bootstrap
import smtplib
import os
#import Mail, Email, To, Content
SUBJECT = "You are in Containment zone"
s = smtplib.SMTP('smtp.gmail.com', 587)
#from sendemail import sendmail,sendgridmail
#import smtplib

app = Flask(__name__)
bootstrap = Bootstrap(app) 
app.secret_key = 'a'

  
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'bGQo0FIi8y'
app.config['MYSQL_PASSWORD'] = 'y7SaG8yR5o'
app.config['MYSQL_DB'] = 'bGQo0FIi8y'
mysql = MySQL(app)
@app.route('/')

def homer():
    return render_template('base.html')

   
@app.route('/log', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
    
        
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tab WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO tab VALUES (NULL, % s, % s, % s)', (username,password,email))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            #TEXT = "Hello "+username + ",\n\n"+ """Thanks for applying registring at smartinterns """ 
            #message  = 'Subject: {}\n\n{}'.format("smartinterns Carrers", TEXT)
            #sendmail(TEXT,email)
            #sendgridmail(email,TEXT)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('log.html', msg = msg)

@app.route('/reg',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tab WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('main.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('signin.html', msg = msg)



@app.route('/loc',methods =['GET', 'POST'])
def display():
    res = requests.get('https://ipinfo.io/')
    data = res.json()

    city = data['city']

    location = data['loc'].split(',')
    latitude = location[0]
    longitude = location[1]
    a = ["chi","Pimpri"]
    if city in a:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("cozo.containmentzone@gmail.com", "covid19cozo")
        TEXT = "Hello "+username + ",\n\n"+ """Thanks for using CoZo app.You are in caontainment zone.Please take care and BE SAFE!!!!!! """ 
        message  = 'Subject: {}\n\n{}'.format("you are in containment zone", TEXT)
        sendmail(TEXT,email)
        s.sendmail("cozo.containmentzone@gmail.com", email, message)
        s.quit()
            #sendgridmail(email,TEXT)
   
   
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port = 8080)