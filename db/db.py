import sqlite3

def authenticate(uname, pword):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    q = "SELECT username, password FROM users"
    result = c.execute(q)
    for r in result:
        if uname == username and pword == password:
            return True
    return False

def insert(email, uname, pword):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    q = "INSERT INTO users (%s, %s, %d)"
    c.execute(q, (email, uname, pword))
