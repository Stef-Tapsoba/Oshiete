import os
from turtle import title
from flask import Flask, render_template, send_from_directory, url_for, request, flash, redirect
import mysql.connector
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = "hellokitty"

#initialize mysql database
mydb = mysql.connector.connect(
    host="127.0.0.1", #db
    port="33065",
    user="root",
    passwd="example",
    database="info600"
)


#Home page
@app.route("/", methods=["POST", "GET"])
@app.route("/home")
def index():
    if request.method == 'POST':
        flash("Thank you for sending this message. We will get back to you as soon as possible.")
    return render_template("index.html", title="Home")


#Sign up page with form to fill out
@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    try:
        if request.method == 'POST':
            #fetch form data
            userDetails = request.form
            username = str(userDetails['inputName'])
            email = str(userDetails['inputEmail'])
            password = str(userDetails['inputPassword'])
            
            #Insert new user to database
            my_cursor = mydb.cursor()
            my_cursor.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", 
                              (username, email, password))
            mydb.commit()
            my_cursor.close()
            flash("Your account has been successfully created! Log in now to start your journey!", "success")
            return redirect(url_for('login'))
            
    except mysql.connector.Error as error:
        print("Failed to insert record")
    return render_template("signup.html", title="Sign Up")


#Sign in page with form t fill out
@app.route("/login")
def login():
    return render_template("login.html", title="Login")


#User profile once they are logged in
@app.route("/user/profile", methods=["POST", "GET"])
def profile():
    flash("Welcome back, "+str(request.form["username"]) +"! Ready to learn?")
    return render_template("profile.html", title="Profile")


@app.route("/user/courses")
def courses():
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT * FROM courses")
    records = my_cursor.fetchall()
    my_cursor.close()
    return render_template("courses.html",courses=records)

#About page
@app.route("/about")
def about():
    return render_template("about.html")


#Contact us page with a form to fill with message
@app.route("/contact")
def contact():
    return render_template("contact.html")


#Used to see the users that are registered
@app.route("/database")
def database():
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT username, email, password FROM users")
    records = my_cursor.fetchall()
    my_cursor.close()
    return render_template("view.html",records=records)
        

#Run program in debug mode
if __name__ == '__main__':
    app.run(debug=True)
    