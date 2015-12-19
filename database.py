import sqlite3
from time import time

def new_user(email, password_hash, first, last):
    """
    new_use: adds a new user to the database, returns False if unsuccessful

    Args:
        email (string): the email of the user
	password_hash (string): the hex string of a hased password
        first (string): the first name of the user
        last (string): the last name of the user
    
    Returns:
        True if successfully added, False otherwise (email has already been
        taken)
    
    Example:
        >>> new_user("alex.wyc2098@gmail.com", "7b77e4d3de87423f0c98716ad54bd2f3", "Yicheng", "Wang")
        True
        >>> new_user("alex.wyc2098@gmail.com", "12354ab6a7e87af879dbadf87124faab", "Yicheng", "Wang")
        False (because the email has already been registered)
    """
    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT users.email
    FROM users
    WHERE users.email = ?"""

    usernames = c.execute(q, (email,)).fetchall()

    if (len(usernames)) == 0:
        q = "INSERT INTO users VALUES (?,?,?,?)"
        c.execute(q, (email, password_hash, first, last))
        conn.commit()
        return True
    
    return False

def authenticate(email, password_hash):
    """
    authenticate: authentics an user login

    Args:
        email (string): the email to authenticate
	password_hash (string): the hash of the password that the user inputed
    
    Returns:
        True if the two match, False otherwise
    
    Example:
        >>> authenticate("alex.wyc2098@gmail.com", "7b77e4d3de87423f0c98716ad54bd2f3")
        True
        >>> authenticate("alex.wyc2098@gmail.com", "12354ab6a7e87af879dbadf87124faab")
        False    
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT users.email, users.password
    FROM users
    WHERE users.email = ? AND users.password = ?"""

    result = c.execute(q, (email, password_hash)).fetchall()

    return (len(result) != 0)

def update_pwd(email, new_password):
    """
    update_pwd: updates password for an user

    Args:
        email (type): TODO
	new_password (type): TODO
    
    Returns:
        True if successful, False otherwise
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT * FROM users WHERE users.email = ?"""

    result = c.execute(q, (email)).fetchall()

    if len(result) == 0:
        return False

    q = """UPDATE users SET users.password = ? WHERE users.email = ?"""

    c.execute(q, (new_password, email))

    conn.commit()
    
    return True

def next_avaliable_id():
    """
    next_a: gives out the next avaliable id for the sites table
    
    Returns:
        an integer that represents the next possible id
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.id FROM sites"""

    result = c.execute(q).fetchall()

    if (len(result) == 0):
        return 0

    if (len(result) == 1):
        return 1

    for i in range(1, len(result)):
        if result[i] - result[i - 1] != 1:
            return result[i - 1] + 1

    return len(result)


def add_to_sites(email, site):
    """
    add_to_sites: add a site to the user's list

    Args:
        email (string): the user
	site (string): the marked up html of the site
    
    Returns:
        True if successful, False otherwise
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """INSERT INTO sites VALUES (?, ?, ?)"""

    try:
        c.execute(q, (next_avaliable_id(), email, site))
        conn.commit()
        return True
    except:
        return False

def get_list_of_sites(email):
    """
    get_list_of_sites: returns a list of sites based on a certain email

    Args:
        email (string): the user
    
    Returns:
        a list of sites formatted in the following manner ranked by last edited
        time:
        [(site-id1, site1), (site-id2, site2), ...]
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.id, sites.site
    FROM sites
    WHERE sites.email = ?
    ORDER BY t DESC"""

    r = c.execute(q, (email,)).fetchall()
    return r

def update_site(email, site_id, new_site):
    """
    update_site: updates the site entry for the user

    Args:
        email (string): the user
	site_id (int): the id of the site in the database
	new_site (string): updated markup for the site
    
    Returns:
        True if successful, False otherwise    
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT * FROM sites WHERE sites.email = ? AND sites.id = ?"""

    result = c.execute(q, (email, site_id)).fetchall()

    if (len(result) == 0):
        return False

    q = """UPDATE sites SET sites.site = ? WHERE sites.id = ?"""

    result = c.execute(q, (new_site, site_id))

    conn.commit()

def delete_site(email, site_id):
    """
    delete_site: deletes a site from the user's "library" according to id

    Args:
        email (string): the user
	site_id (int): id of the site
    
    Returns:
        True if successful, False otherwise
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT * FROM sites WHERE sites.email = ? AND sites.id = ?"""

    result = c.execute(q, (email, site_id)).fetchall()

    if (len(result) == 0):
        return False

    q = """REMOVE FROM sites WHERE sites.id = ?"""

    c.execute(q, (site_id,))

    conn.commit()
