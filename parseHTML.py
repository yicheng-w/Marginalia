#################################################################################
# Parse HTML for the project, handles the BeautifulSoup and HTML that is passed #
# and connects it to the database                                               #
#                                                                               #
# Authors                                                                       #
#  Jeffrey Zou                                                                  #
#                                                                               #
# Description                                                                   #
#  Handles the formatting of the HTML                                           #
#                                                                               #
#################################################################################

import sqlite3
from bs4 import BeautifulSoup
from database import *
import json
from flask import Response, json, Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.config.from_object(__name__)

print "hi"

@app.route("/", methods = ['GET', 'POST']) # adds a site to a user's collection, site passed via POST request, user info stored in session
#@login_required
def api_add_site():
    print "inside app route"
    site = request.form['site']
    site = BeautifulSoup(site).encode("utf-8");
    print site
    print "middle"
    #print site
    print "afterwards"
    if request.method == 'GET':
        flash("failed!")
        return json.dumps({'status': 'failure', 'msg': 'Incorrect request method'})

    #email = session['email']
    print "email and site"
    print site
    '''
    if add_to_sites(email, site):
        flash("succeeded!")
        return json.dumps({"status": 'success', 'msg': 'Your site has been successfully added'})
'''
    return json.dumps({"status": 'failure', 'msg': 'Something went wrong :('})



def pretty(htmlPage):
    '''
    Returns a pretty version of the HTML

    Args:
        htmlPage (string): the HTML that will be prettified

    Returns:
        Unicode of prettified HTML
    '''

    soup = BeautifulSoup(htmlPage, "html.parser")
    return soup.prettify()

def updateDatabase(email, htmlPage, site_id, comments, notes):
    '''
    Updates the database with the page or adds it if it does not exist

    Args:
        htmlPage (string): the HTML of the page
        email (string): user's email
        site_id (integer): id of the site, -1 if it does not exist

    Returns:
        True
    '''

    page = pretty(htmlPage)
    if site_id == -1:
        add_to_sites(email, page, comments, notes)
    else:
        update_site(email, site_id, page, comments, notes)
    return True

print "hello"

'''
class MyRequestHandler():
    def get(self):
        result = {pretty(self.data)}
        json_obj = json.dumps(result)
        print result
        self.response.out.write(str(json_obj))
'''


if __name__ == "__main__":
    try:
        app.secret_key = 'hello'
    except ValueError:
        app.secret_key = "nvm ariel i was dumb"

    app.run(host = "0.0.0.0", port = 8000, debug = ("--debug"))

