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
#  Testing to make sure everything works
#  Write error.html

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

@app.route("/register", methods = ["GET", 'POST'])
def register():
    if request.method == "GET":
        return json.dumps({'status': 'failure', 'msg': 'Incorrect login method'})

    else:
        email = request.form['email']
        password = request.form['password']
        first = request.form['first']
        last = request.form['last']

        m = hashlib.sha256()
        m.update(password)
        passhash = m.hexdigest()

        if new_user(email, passhash, first, last):
            return json.dumps({'status': 'success', 'msg': 'You have successfully registered an account, please log-in to continue'})
        else:
            return json.dumps({'status': 'failure', 'msg': 'Email already in use'})

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return json.dumps({'status': 'failure', "msg": 'Incorrect login method'})

    else:
        email = request.form['email']
        password = request.form['password']

        m = hashlib.sha256()
        m.update(password)
        passhash = m.hexdigest()

        if (authenticate(email, passhash)):
            session["email"] = email
            return json.dumps({'status': 'success', 'msg': 'you are now logged in'})
        else:
            return json.dumps({'status': 'failure', 'msg': 'incorrect email and password combination'})

@app.route("/change_pwd", methods = ["GET", 'POST'])
def change_pwd():
    # TODO jeffrey!
    return

@app.route("/view") # view all sites of a user, username stored in cookie
@login_required
def view_static():
    email = session['email']
    list_of_sites = get_list_of_sites(email)
    return json.dumps({'status': 'success', 'result': list_of_sites})

@app.route("/view/<int:id>") # grab a specific story based on id
@login_required
def view_site(id):
    email = session['email']
    list_of_sites = get_list_of_sites(email)
    for site in list_of_sites:
        if site[0] == id:
            return json.dumps({'status': 'success', 'result': site[1]})
    
    return json.dumps({'status': 'failure', 'msg': 'the site you requested does not exist'})

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

@app.route("/delete/<int:id>") # deletes a story based on id, user data stored in session
@login_required
def api_delete_site(id):
    email = session['email']
    
    if delete_site(email, id):
        return json.dumps({'status': 'success', 'msg': 'Your site has been successfully deleted'})

    return json.dumps({'status': 'failure', 'msg': 'Something went wrong :('})

@app.route("/share/<int:id>") # ONLY NON-JSON FUNCTION, ACTUALLY RENDERS THE SHARED SITE
def share(id):
    site = get_site_for_sharing(id)

    if site:
        return render_template(site)

    else:
        return render_template("error.html") # TODO

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, debug = ("--debug" in argv))
