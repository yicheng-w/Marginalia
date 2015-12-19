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

conn = sqlite3.connect("./db/infos.db")

c = conn.cursor()

create_base = "CREATE TABLE %s (%s)" # no user input needed, use %s

 # password = hexstring of hash
c.execute(create_base % ("users", "email TEXT, password TEXT, first TEXT, last TEXT"))

# note will be html source code with markup
c.execute(create_base % ("sites", "id INTEGER, email TEXT, site TEXT, t INTEGER"))

conn.commit()
