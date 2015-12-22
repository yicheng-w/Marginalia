################################################################################
# Backend Database management for Annotation project                           #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang                                                                #
#                                                                              #
# Description                                                                  #
#  Deals with database in various fashion                                      #
#                                                                              #
################################################################################

# TODO
#  TODO-List

# Dev Log
#  Project Created: 2015-12-19 15:00 - Yicheng W.

import sqlite3
from time import time, sleep

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
    authenticate: authenticates an user login

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

    result = c.execute(q, (email,)).fetchall()

    if len(result) == 0:
        return False

    q = """UPDATE users SET password = ? WHERE email = ?"""

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

    print result

    if (len(result) == 0):
        return 0

    if (len(result) == 1):
        return 1

    for i in range(1, len(result)):
        if result[i][0] - result[i - 1][0] != 1:
            return result[i - 1][0] + 1

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

    q = """INSERT INTO sites VALUES (?, ?, ?, ?, ?)"""

    c.execute(q, (next_avaliable_id(), email, site, 0, int(time()))) # default permission is private
    conn.commit()

def get_list_of_sites(email):
    """
    get_list_of_sites: returns a list of sites based on a certain email

    Args:
        email (string): the user
    
    Returns:
        a list of sites formatted in the following manner ranked by last edited
        time:
        [(site-id1, site1, permission1), (site-id2, site2, permission2), ...]
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.id, sites.site, sites.shared
    FROM sites
    WHERE sites.email = ?
    ORDER BY t DESC"""

    r = c.execute(q, (email,)).fetchall()
    return r

def get_site_for_sharing(id):
    """
    get_site_for_sharing: get the content of one site for sharing, returns None
    if the site doesn't exist or is private

    Args:
        id (int): the ID of the site
    
    Returns:
        the content of the site if the retrival was successful, None if the
        site-id doesn't exist or is private    
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.shared, sites.site
    FROM sites
    WHERE sites.id = ?"""

    r = c.execute(q, (id, )).fetchall()

    if (len(r) == 0):
        return None

    if (r[0][0] == 0): # if the site is private
        return None

    return r[0][1]

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

    q = """UPDATE sites SET site = ?, t = ? WHERE id = ?"""

    c.execute(q, (new_site, int(time()), site_id))

    conn.commit()

    return True

def change_site_permission(email, id):
    """
    change_site_permission: changes the permission of a site (public -> private
    or private -> public)

    Args:
        email (string): the user
	id (int): the id of the site
    
    Returns:
        True if successful, False if the id and the email doesn't match
    """

    conn = sqlite3.connect('./db/infos.db')
    c = conn.cursor()

    q = """SELECT sites.shared
    FROM sites
    WHERE sites.email = ? AND sites.id = ?"""

    r = c.execute(q).fetchall()

    if (len(r) != 1):
        return False

    q = """UPDATE sites
    SET shared = ?
    WHERE id = ?"""

    if (r[0][0] == 0): # used to be private, now becomes public
        c.execute(q, (1, id))
    else: # used to be public, now becomes private
        c.execute(q, (0, id))

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

    q = """DELETE FROM sites WHERE sites.id = ?"""

    c.execute(q, (site_id,))

    conn.commit()

    return True




if __name__ == "__main__":
    print "new_user test"
    print new_user("alex.wyc2098@gmail.com", "12345", "Yicheng", "Wang")
    print new_user("alex.wyc2098@gmail.com", "dgjsadkfhsa", "Yicheng", "Wang")
    print new_user("alex.wyc2098@protonmail.ch", "ajdfsadfk", "Yicheng", "Wang")

    print "\nauthentication test"
    print authenticate("alex.wyc2098@gmail.com", "12345")
    print authenticate("alex.wyc2098@protonmail.ch", "12345")
    print authenticate("asdf@asdf.asdf", "12435")

    print "\nchange password test"
    print update_pwd("alex.wyc2098@gmail.com", "54321")
    print update_pwd("asdf@asdf.com", "12345")

    print authenticate("alex.wyc2098@gmail.com", "12345")
    print authenticate("alex.wyc2098@gmail.com", "54321")

    print "\nadd_to_sites test"
    print add_to_sites("alex.wyc2098@gmail.com", "123456789")
    print add_to_sites("alex.wyc2098@protonmail.ch", "fkjhsadgfkvasv")
    print add_to_sites("alex.wyc2098@gmail.com", "12hsadffghas")

    print get_list_of_sites("alex.wyc2098@gmail.com")
    print get_list_of_sites("alex.wyc2098@protonmail.ch")

    sleep(1)

    print "\nupdate_site test"
    print update_site("alex.wyc2098@gmail.com", "0", "new_site!")

    print get_list_of_sites("alex.wyc2098@gmail.com")

    print "\ndelete_site test"
    print delete_site("alex.wyc2098@gmail.com", 2)
    print delete_site("alex.wyc2098@gmail.com", 3)
    
    print add_to_sites("alex.wyc2098@gmail.com", "this is the new site 2")
    
    print get_list_of_sites("alex.wyc2098@gmail.com")