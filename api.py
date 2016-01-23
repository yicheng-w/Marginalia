###############################################################################
# API for the Annotation project, handles AJAX calls and gives out JSON        #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang, Jeffrey Zou, Alice Xue                                        #
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
#  Connected to the chrome extension: 2016-1-21 20:52 - Alice X.

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
from bs4 import BeautifulSoup
import unicodedata

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return render_template("login.html", err = "You must login to continue.")
        return f(*args, **kwargs)
    return decorated_function

def login_required_api(f):
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
        return render_template("index.html", name = session['name'])

    return render_template("index.html")

@app.route("/about")
def about():
    if 'name' in session:
        return render_template("about.html", name = session['name'])

    return render_template("about.html")

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
            return render_template("register.html", status = "success")
            # in register.html redirect them to login
        else:
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
            session['name'] = get_name_from_email(email)
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

        return render_template("forget_pwd.html", status = "success")

@app.route("/change_pwd")
@login_required
def change_pwd_page():
    return render_template("change_pwd.html", name = session['name'])

@app.route("/change_pwd", methods = ["GET", 'POST'])
@login_required
def change_pwd():
    if request.method == "GET":
        return redirect(url_for("change_password"))
    else:
        email = session['email']
        old_password = request.form['oldpass']

        m = sha256()
        m.update(old_password)
        passhash = m.hexdigest()
        if (authenticate(email,passhash)):
            new_password = request.form['newpass']
            confirmed = request.form['confirm']

            if new_password != confirmed:
                return render_template("change_pwd.html", err = "The new password did match its confirmation", name = session['name'])

            m = sha256()
            m.update(new_password)
            newhashed = m.hexdigest()
            changed = update_pwd(email, newhashed)
            if changed:
                return render_template("change_pwd.html", status = "success", name = session['name'])
            else:
                return render_template("change_pwd.html", err = "There was a problem in changing the password", name = session['name'])
        else:
            return render_template("change_pwd.html", err = "Incorrect old password", name = session['name'])

@app.route("/view") # view all sites of a user, username stored in cookie
@login_required
def view_static():
    email = session['email']
    list_of_sites = get_list_of_sites(email)
    return render_template("view.html", sites = list_of_sites, name = session['name'])

@app.route("/view/<int:id>") # grab a specific story based on id
@login_required
def view_site(id):
    email = session['email']
    site = get_site_on_id(email, id)

    if (site):
        return render_template("view_one.html", site = site, name = session['name'])

    return render_template("error.html", msg = "Sorry but the site you're looking for does not exist or belong to you", name = session['name'])

@app.route("/view/test")
def view_test():
    return render_template("view_test.html", name = session['name'])

@app.route("/search", methods = ['GET'])
@login_required
def search():
    search_string = request.args.get('search', '')
    result = search_user_sites(session['email'], search_string)

    print result
    return "lol"

@app.route("/logout")
@login_required
def logout():
    del session['email']
    del session['name']
    return redirect(url_for("home"))

@app.route("/share/<int:id>") # reders the site if shares, gives out error otherwise
def share(id):
    site = get_site_for_sharing(id)

    if site:
        if 'name' in session:
            return render_template("view_one.html", site = site, name = session['name'])
        else:
            return render_template("view_one.html", site = site)

    elif 'name' in session:
        return render_template("error.html", msg = "Sorry this site is not up for sharing &nbsp;:(", name = session['name']);
    
    else:
        return render_template("error.html", msg = "Sorry this site is not up for sharing:(")

### API CALLS -------------------------------------------------------------####

@app.route("/new/", methods = ['GET', 'POST']) # adds a site to a user's collection, site passed via POST request, user info stored in session
@login_required_api
def api_add_site():
    if request.method == 'GET':
        return json.dumps({'status': 'failure', 'msg': 'Incorrect request method'})
    
    email = session['email']
    title = request.form['title']
    author = request.form['author']
    date = request.form['date']
    site = request.form['site']
    url = request.form['url']

    soup = BeautifulSoup(site, 'html.parser')
    articles = soup.find_all("article")
    
    maxArticle = articles[0]
    for i in articles:
        if len(str(i)) > len(str(maxArticle)):
            maxArticle = i
    
    paragraphs = maxArticle.find_all("p")
    
 
    site = "<p>"
    for i in paragraphs:
        #print type(i)
        #print i.contents
        #print type(i.text)
        
        site = site + i.text + "</p>\n<p>"  
        
    
    htmlsite = "<a href=" + url + "><h4>" + title + "</h4></a>\n<p>" + author + "</p><p>" + date + "</p>" + site + "</p>"
    
     
    if add_to_sites(email, title, htmlsite, "", ""):
        return json.dumps({"status": 'success', 'msg': 'Your site has been successfully added'})

    return json.dumps({"status": 'failure', 'msg': 'Something went wrong :('})

@app.route("/update/<int:id>", methods = ["GET", 'POST']) # update a specific site based on id, new site content passed via POST request, user info stored in session
@login_required_api
def api_update_site(id):
    if request.method == 'GET':
        return json.dumps({"status": 'failure', 'msg': 'Incorrect request method'})
    email = session['email']
    new_site = request.form['site']
    new_comments = request.form['comment']
    new_notes = request.form['note']
    if update_site(email, id, new_site, new_comments, new_notes):
        return json.dumps({"status": 'success', 'msg': 'Your marks have been updated'})

    return json.dumps({'status': 'failure', 'msg': "Something went wrong :("})

@app.route("/change_perm/", methods = ['GET', 'POST']) # changes sharing permission for a site, user info stored in session
@login_required_api
def api_change_perm():
    if request.method == 'GET':
        return json.dumps({'status':'failure', 'msg': 'Something went wrong :('})

    email = session['email']
    id = int(request.form['id'])
    if change_site_permission(email, id):
        return json.dumps({"status": 'success', 'msg': "The permission of your site has been successfully changed", 'to': request.form['to'], 'id': id})

    return json.dumps({'status': 'failure', 'msg': 'Something went wrong :('})

@app.route("/delete/", methods = ['GET', 'POST']) # deletes a story based on id, user data stored in session
@login_required_api
def api_delete_site():
    if request.method == 'GET':
        return json.dumps({'status':'failure', 'msg': 'Something went wrong :('})

    email = session['email']
    id = request.form['id']

    if delete_site(email, id):
        return json.dumps({'status': 'success', 'msg': 'Your site has been successfully deleted'})

    return json.dumps({'status': 'failure', 'msg': 'Something went wrong :('})

@app.route("/fork/<int:id>") # copies a shared document into own's own private repo
# relatively low priority but still on TODO
@login_required_api
def fork(id):
    email = session['email']
    
    if fork_shared_site(id, email):
        return json.dumps({'status': 'success', 'msg':'The site has been successfully added to your own library'})

    return json.dumps({'status': 'failure', 'msg': 'Something went wrong'})

if __name__ == "__main__":
    try:
        app.secret_key = argv[argv.index('--key') + 1]
    except ValueError:
        app.secret_key = "nvm ariel i was dumb"

    app.run(host = "0.0.0.0", port = 8000, debug = ("--debug" in argv))
