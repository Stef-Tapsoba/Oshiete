import os
from turtle import title
from flask import Flask, render_template, send_from_directory, url_for, request, flash, redirect
import mysql.connector
from datetime import datetime
import re
from forms import registration_form, login_form

app = Flask(__name__)
app.secret_key = "hellokitty"

@app.route("/", methods=["POST", "GET"])
@app.route("/home")
def index():
    return render_template("index.html", title="Home")

@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    form = registration_form()
    if form.validate_on_submit():
        flash(f"Good news, {form.username.data}! You've successfully created an account!", "success")
        return redirect(url_for('index'))
    return render_template("signup.html", title="Sign Up", form=form)

@app.route("/login")
def login():
    form = login_form()
    return render_template("login.html", title="Login", form=form)

@app.route("/user/profile", methods=["POST", "GET"])
def profile():
    flash("Welcome back, "+str(request.form["username"]) +"! Ready to learn?")
    return render_template("profile.html", title="Profile")
    """
def profile(username):
    #request.form['username']
    #flash("Youkoso")
    return render_template("hello.html", name=username)
    """

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/database")
def database():
    mydb = mysql.connector.connect(
        host="db",
        port="33065",
        user="root",
        passwd="example",
        database="info600"
    )
    
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT name, email FROM users")
    records = my_cursor.fetchall()

    return render_template("view.html",records=records)

if __name__ == '__main__':
    app.run(debug=True)
    