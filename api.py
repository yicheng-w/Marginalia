################################################################################
# API for the Annotation project, handles AJAX calls and gives out JSON        #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang, Jeffrey Zou                                                   #
#                                                                              #
# Description                                                                  #
#  Handles AJAX calls and database management                                  #
#                                                                              #
################################################################################

# TODO
#  Jeffrey can you implement the change password function? See below in change_pwd
#  Write all the htmls
#  Write a bunch of server-side stuff, such as home page, about, etc and stuff
#  Testing to make sure everything works

# Dev Log
#  Project Created: 2015-12-19 14:57 - Yicheng W.
#  Most API stuff are done: 2015-12-20 18:23 - Yicheng W.
#  Template inheritance and basic HTML setup: 2015-12-27 17:17 - Ariel L.

from flask import Flask, request, render_template, session, redirect, url_for
from database import *
from functools import wraps
from hashlib import sha256
import json
from sys import argv
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import choice
from string import ascii_letters, digits

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return json.dumps({'status': 'failure', 'error': 'Login Required'})
        return f(*args, **kwargs)
    return decorated_function

co_email = "marginalia.overlords@gmail.com"
co_pass = open("password.txt", 'r').read()[:-1]
alphabet = ascii_letters + digits

### HTML CALLS-------------------------------------------------------------####

@app.route("/")
@app.route("/home")
def home():
    # TODO this should have two versions, one version where the user is logged
    # in, one version in which the user is not logged in
    # if the user is logged in, this page should display his/her marked sites,
    # otherwise it should be an ad-page with login infos
    if 'email' in session:
        return render_template("index.html", email = session['email'])

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html") # TODO

@app.route("/regist") # this is actually the register page
def register_page():
    return render_template("register.html") 

@app.route("/login") # login page
def login_page():
    return render_template("login.html") 

@app.route("/register", methods = ["GET", 'POST'])
def register():
    if request.method == "GET":
        return redirect(url_for("register_page"))

    else:
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        first = request.form['first']
        last = request.form['last']

        if email == "":
            return render_template("register.html", err = "Please enter your email!")

        if password == "":
            return render_template("register.html", err = "Password cannot be empty!")

        if password != confirm:
            return render_template("register.html", err = "Password does not match the confirm password!")

        if first == "" or last == "":
            return render_template("register.html", err = "Please enter your name!")

        m = sha256()
        m.update(password)
        passhash = m.hexdigest()

        if new_user(email, passhash, first, last):
            print "success"
            return render_template("register.html", status = "success")
            # in register.html redirect them to login
        else:
            print "failed"
            return render_template("register.html", err = "Email already in use!")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect(url_for("login_page"))

    else:
        email = request.form['email']
        password = request.form['password']

        m = sha256()
        m.update(password)
        passhash = m.hexdigest()

        if (authenticate(email, passhash)):
            session["email"] = email
            return redirect(url_for("home"))
        else:
            return render_template("login.html", err = "Incorrect email/password combination")

@app.route("/forget_pwd")
def forget_pwd_page():
    return render_template("forget_pwd.html")

@app.route("/forget_pwd", methods = ["GET", 'POST'])
def forget_pwd():
    if request.method == "GET":
        return redirect(url_for("forget_pwd_page"))

    else:
        email = request.form['email']
        new_pass = ''.join(choice(alphabet) for i in range(10))

        print "asdjfhasjdklfhal"

        m = sha256()
        m.update(new_pass)
        passhash = m.hexdigest()

        if not update_pwd(email, passhash):
            return render_template("forget_pwd.html", err = "The email you entered is not registered")

        s = SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(co_email, co_pass)

        msg = """To: %s
From: %s
Subject: Marginalia Password Change Request

Dear %s,

You have requested a password change, here is your new password: %s

If you did not request this change, please still login and then change your password immediately. If this persists, please email us at marginalia.overlords@gmail.com

Sincerely,
The Marginalia Overlords""" % (email, co_email, get_name_from_email(email), new_pass)

        s.sendmail(co_email, email, msg)
        s.close()

        print "adjksfhsalkjd"
        return render_template("forget_pwd.html", status = "success")

@app.route("/change_pwd")
@login_required
def change_pwd_page():
    return render_template("change_pwd.html", email = session['email'])

@app.route("/change_pwd", methods = ["GET", 'POST'])
@login_required
def change_pwd():
    if request.method == "GET":
        return redirect(url_for("change_password"))
    else:
        email = request.form['email']
        old_password = request.form['oldpass']

        m = sha256()
        m.update(old_password)
        passhash = m.hexdigest()
        if (authenticate(email,passhash)):
            new_password = request.form['newpass']
            newhashed = haslib.sha256().update(new_password).hexdigest()
            changed = update_pwd(email, newhashed)
            if changed:
                return redirect("change_pwd.html", status = "success", email = session['email'])
            else:
                return render_template("change_pwd.html", err = "There was a problem in changing the password", email = session['email'])
        else:
            return render_template("change_pwd.html", err = "Incorrect old password", email = session['email'])

@app.route("/view") # view all sites of a user, username stored in cookie
@login_required
def view_static():
    email = session['email']
    list_of_sites = get_list_of_sites(email)
    return render_template("view.html", sites = list_of_sites, email = email)

@app.route("/view/<int:id>") # grab a specific story based on id
@login_required
def view_site(id):
    email = session['email']
    list_of_sites = get_list_of_sites(email)
    for site in list_of_sites:
        if site[0] == id:
            return render_template("view_one.html", site=site[1], shared=site[2], email = email)

    return render_template("error.html", msg = "Sorry but the site you're looking for does not exist or belong to you", email = email)

@app.route("/logout")
@login_required
def logout():
    del session['email']
    return redirect(url_for("home"))

@app.route("/share/<int:id>") # reders the site if shares, gives out error otherwise
def share(id):
    site = get_site_for_sharing(id)

    if site:
        return render_template("view_one.html", site = site, email = email)

    else:
        return render_template("error.html", msg = "Sorry this site is not up for sharing :(", email = email);

### API CALLS -------------------------------------------------------------####

@app.route("/new/", methods = ['GET', 'POST']) # adds a site to a user's collection, site passed via POST request, user info stored in session
@login_required
def api_add_site():
    if request.method == 'GET':
        return json.dumps({'status': 'failure', 'msg': 'Incorrect request method'})

    email = session['email']
    site = request.form['site']

    if add_to_sites(email, site):
        return json.dumps({"status": 'success', 'msg': 'Your site has been successfully added'})

    return json.dumps({"status": 'failure', 'msg': 'Something went wrong :('})

@app.route("/update/<int:id>", methods = ["GET", 'POST']) # update a specific site based on id, new site content passed via POST request, user info stored in session
@login_required
def api_update_site(id):
    if request.method == 'GET':
        return json.dumps({"status": 'failure', 'msg': 'Incorrect request method'})
    email = session['email']
    new_site = request.form['new_site']
    if update_site(email, id, new_site):
        return json.dumps({"status": 'success', 'msg': 'Your marks have been updated'})

    return json.dumps({'status': 'failure', 'msg': "Something went wrong :("})

@app.route("/change_perm/<int:id>") # changes sharing permission for a site, user info stored in session
@login_required
def api_change_perm(id):
    email = session['email']
    if change_site_permission(email, id):
        return json.dumps({"status": 'success', 'msg': "The permission of your site has been successfully changed"})

    return json.dumps({'status': 'failure', 'msg': 'Something went wrong :('})

@app.route("/delete/<int:id>") # deletes a story based on id, user data stored in session
@login_required
def api_delete_site(id):
    email = session['email']

    if delete_site(email, id):
        return json.dumps({'status': 'success', 'msg': 'Your site has been successfully deleted'})

    return json.dumps({'status': 'failure', 'msg': 'Something went wrong :('})

if __name__ == "__main__":
    try:
        app.secret_key = argv[argv.index('--key') + 1]
    except ValueError:
        app.secret_key = "nvm ariel i was dumb"

    app.run(host = "0.0.0.0", port = 8000, debug = ("--debug" in argv))
