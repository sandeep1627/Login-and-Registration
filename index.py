from flask import Flask,render_template,request,redirect,jsonify,make_response,session
import jwt
from datetime import datetime,timedelta
import mysql.connector
from functools import wraps
import time

web=Flask(__name__)
web.config["SECRET_KEY"]="271e22dca770443ba6cc04f514560cfc"

def required_token(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token=request/args.get(token)
        if not token:
            return jsonify({'Alert':'Token is missing'})
        try:
            payload=jwt.decode(token,web.config['SECRET_KEY'])
        except:
            return jsonify({'Alert':'Not a valid token'})
        return decorated


connect=mysql.connector.connect(host="localhost",user="root",password="",database="sandeep")
cursor=connect.cursor()
@web.route('/')
def home():
    return render_template("login.html")

@web.route('/registration')
def registration():
    return render_template("registration.html")

@required_token
@web.route('/validation',methods=['post'])
def validation():
    email=request.form.get('email')
    password=request.form.get('password')
    query="SELECT email,password FROM details where email='{}' and password='{}'".format(email,password)
    cursor.execute(query)
    result=cursor.fetchall()
    if (len(result)>0):
        token=jwt.encode({
            'user':request.form.get('email'),
            'expiration':str(datetime.utcnow()+timedelta(seconds=2))
        }
        ,   web.config['SECRET_KEY'])
        return render_template("logged_in.html")
    else:
        return render_template("registration.html")
    connect.commit()

@required_token
@web.route('/logged_in')
def logged_in():
    return render_template("logged_in.html")

@web.route('/add_user',methods=['post'])
def add_user():
    first_name=request.form.get('fname')
    last_name=request.form.get('lname')
    mobile=request.form.get('mobile')
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""INSERT INTO `details`(`First Name`, `Last Name`, `mobile`, `email`, `password`) VALUES ('{}','{}','{}','{}','{}')""".format(first_name,last_name,mobile,email,password))
    connect.commit()
    return "User Successfully Registered"
if __name__=="__main__":
    web.run(debug=True)