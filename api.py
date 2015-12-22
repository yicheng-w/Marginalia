################################################################################
# API for the Annotation project, handles AJAX calls and gives out JSON        #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang                                                                #
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

from flask import Flask, request, render_template, session, redirect, url_for
from database import *
from functools import wraps
from hashlib import sha256
import json
from sys import argv

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return json.dumps({'status': 'failure', 'error': 'Login Required'})
        return f(*args, **kwargs)
    return decorated_function

### HTML CALLS-------------------------------------------------------------####

@app.route("/")
@app.route("/home")
def home():
    # TODO this should have two versions, one version where the user is logged
    # in, one version in which the user is not logged in
    # if the user is logged in, this page should display his/her marked sites,
    # otherwise it should be an ad-page with login infos
    return

@app.route("/about")
def about():
    return render_template("about.html") # TODO

@app.route("/regist") # this is actually the register page
def register_page():
    return render_template("register.html") # TODO

@app.route("/login") # login page
def login_page():
    return render_template("login.html") # TODO

@app.route("/register", methods = ["GET", 'POST'])
def register():
    if request.method == "GET":
        return redirect(url_for("register_page"))

    else:
        email = request.form['email']
        password = request.form['password']
        first = request.form['first']
        last = request.form['last']

        m = hashlib.sha256()
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

        m = hashlib.sha256()
        m.update(password)
        passhash = m.hexdigest()

        if (authenticate(email, passhash)):
            session["email"] = email
            return redirect(url_for("home"))
        else:
            return render_template("login.html", err = "Incorrect email/password combination")

@app.route("/change_pwd", methods = ["GET", 'POST'])
def change_pwd():
    # TODO jeffrey!
    if request.method = "GET":
        return redirect(url_for(change_password))
    else:
        email = request.form['email']
        old_password = request.form['oldpass']

        m = hashlib.sha256()
        m.update(old_password)
        passhash = m.hexdigest()
        if (authenticate(email,passhash)):
            new_password = request.form['newpass']
            newhashed = haslib.sha256().update(new_password).hexdigest()
            changed = update_pwd(email, newhashed)
            if changed:
                return redirect(url_for("home"))
            else:
                return render_template("changed.html", err = "There was a problem in changing the password")
        else:
            return render_template("changed.html", err = "Incorrect email/password combination")

@app.route("/view") # view all sites of a user, username stored in cookie
@login_required
def view_static():
    email = session['email']
    list_of_sites = get_list_of_sites(email)
    return render_template("view.html", sites = list_of_sites)

@app.route("/view/<int:id>") # grab a specific story based on id
@login_required
def view_site(id):
    email = session['email']
    list_of_sites = get_list_of_sites(email)
    for site in list_of_sites:
        if site[0] == id:
            return render_template("view_one.html", site=site[1], shared=site[2])

    return render_template("error.html", msg = "Sorry but the site you're looking for does not exist or belong to you")

@app.route("/share/<int:id>") # reders the site if shares, gives out error otherwise
def share(id):
    site = get_site_for_sharing(id)

    if site:
        return render_template(site)

    else:
        return render_template("error.html", msg = "Sorry this site is not up for sharing :(")

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
    app.secret_key = argv[argv.index('--key') + 1]
    app.run(host = "0.0.0.0", port = 8000, debug = ("--debug" in argv))
