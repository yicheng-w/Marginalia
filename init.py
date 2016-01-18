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

# TODO
#  create tables

# Dev Log
#  Project Created: 2015-12-19 12:42 - Yicheng W.

import sqlite3
from hashlib import sha256

conn = sqlite3.connect("./db/infos.db")

c = conn.cursor()

create_base = "CREATE TABLE %s (%s)" # no user input needed, use %s

 # password = hexstring of hash
c.execute(create_base % ("users", "email TEXT, password TEXT, first TEXT, last TEXT"))

# note will be html source code with markup
c.execute(create_base % ("sites", "id INTEGER, email TEXT, site TEXT, comments TEXT, notes TEXT, shared INTEGER, t INTEGER"))

conn.commit()

m = sha256()
m.update("12345")
hash = m.hexdigest()

q = """INSERT INTO users VALUES (?, ?, ?, ?)"""

c.execute(q, ('alex.wyc2098@gmail.com', hash, 'Yicheng', 'Wang'))

conn.commit()

q = """INSERT INTO sites VALUES (?, ?, ?, )"""
