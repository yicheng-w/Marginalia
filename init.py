################################################################################
# Initializes the database for user login/storage                              #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang                                                                #
#                                                                              #
# Description                                                                  #
#  Initializes database in db/ for user login and storage                      #
#                                                                              #
################################################################################

# Dev Log
#  Project Created: 2015-12-19 12:42 - Yicheng W.

import sqlite3
from hashlib import sha256
from database import *
from sys import argv

conn = sqlite3.connect("./db/infos.db")

c = conn.cursor()

create_base = "CREATE TABLE %s (%s)" # no user input needed, use %s

 # password = hexstring of hash
c.execute(create_base % ("users", "email TEXT, password TEXT, first TEXT, last TEXT"))

# note will be html source code with markup
c.execute(create_base % ("sites", "id INTEGER, email TEXT, title TEXT, site TEXT, comments TEXT, notes TEXT, shared INTEGER, t INTEGER"))

if '--test' in argv or '-t' in argv:
    m = sha256()
    m.update("12345")
    password = m.hexdigest()

    c.execute('insert into users values("alex.wyc2098@gmail.com", "%s", "Yicheng", "Wang")' % password)
    c.execute('insert into sites values(0, "alex.wyc2098@gmail.com", "test", "test", "", "", 0, 0)')

conn.commit()
