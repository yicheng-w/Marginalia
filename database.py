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
from search import *
from bs4 import BeautifulSoup

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
        email (string): the user
	new_password (string): the new password
    
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

def get_name_from_email(email):
    """
    get_name_from_email: returns the name of the client based on the email
    entered

    Args:
        email (string): the email you are looking for
    
    Returns:
        a string of the form "first last", empty string if the email doesn't
        exist
    
    Example:
        get_name_from_email("alex.wyc2098@gmail.com") --> Yicheng Wang    
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT users.first, users.last FROM users WHERE users.email = ?"""

    result = c.execute(q, (email,)).fetchall()

    if len(result) == 0:
        return ""

    return result[0][0] + " " + result[0][1]

def next_avaliable_id():
    """
    next_a: gives out the next avaliable id for the sites table
    
    Returns:
        an integer that represents the next possible id
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.id FROM sites ORDER BY sites.id"""

    result = c.execute(q).fetchall()

    #print result

    if (len(result) == 0):
        return 0

    if (len(result) == 1):
        return 1

    for i in range(1, len(result)):
        if result[i][0] - result[i - 1][0] != 1:
            return result[i - 1][0] + 1

    return len(result)

def add_to_sites(email, title, site, comments, notes):
    """
    add_to_sites: add a site to the user's list

    Args:
        email (string): the user
        title (string): title of the site
	site (string): the html of the site
        comments (string): the comments on the site
        notes (string): the notes on the site
    
    Returns:
        the id of the new site if successful, -1 otherwise
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """INSERT INTO sites VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

    id = next_avaliable_id()
    c.execute(q, (id, email, title, site, comments, notes, 0, int(time()))) # default permission is private
    conn.commit()
    return id

def get_list_of_sites(email):
    """
    get_list_of_sites: returns a list of sites based on a certain email

    Args:
        email (string): the user
    
    Returns:
        a list of sites formatted in the following manner ranked by last edited
        time:
        [(site-id1, site-title1, permission1), (site-id2, site-title2, permission2), ...]
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.id, sites.title, sites.shared
    FROM sites
    WHERE sites.email = ?
    ORDER BY t DESC"""

    r = c.execute(q, (email,)).fetchall()
    return r

def get_site_on_id(email, id):
    """
    get_site_on_id: get the site title, site, the notes and the comments

    Args:
        email (string): the user
	id (int): the site id
    
    Returns:
        a tuple in the form of:
        (title, site, notes, comments)

        or none if retrival was not successful
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.title, sites.site, sites.notes, sites.comments
    FROM sites
    WHERE sites.email = ? AND sites.id = ?"""

    r = c.execute(q, (email, id)).fetchall()
    
    #print len(r)

    #for i in r:
    #    print i[0]
    #print r

    if (len(r) != 1):
        return None

    return r[0]

def get_site_for_sharing(id):
    """
    get_site_for_sharing: get the content of one site for sharing, returns None
    if the site doesn't exist or is private

    Args:
        id (int): the ID of the site
    
    Returns:
        a tuple in the form of:
        (title, site, notes, comments)

        or none if retrival was not successful
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.title, sites.site, sites.notes,
    sites.comments
    FROM sites
    WHERE sites.id = ? AND sites.shared = 1"""

    r = c.execute(q, (id, )).fetchall()

    if (len(r) == 0):
        return None

    else:
        return r[0]

def update_site(email, site_id, new_site, new_comments, new_notes):
    """
    update_site: updates the site entry for the user

    Args:
        email (string): the user
	site_id (int): the id of the site in the database
	new_site (string): updated markup for the site
        new_comments (string): updated comments for the site
        new_notes (string): updated notes for the site
    
    Returns:
        True if successful, False otherwise    
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT * FROM sites WHERE sites.email = ? AND sites.id = ?"""

    result = c.execute(q, (email, site_id)).fetchall()

    if (len(result) == 0):
        return False

    q = """UPDATE sites SET site = ?, comments = ?, notes = ?, t = ? WHERE id = ?"""

    c.execute(q, (new_site, new_comments, new_notes, int(time()), site_id))

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

    r = c.execute(q, (email, id)).fetchall()

    if (len(r) == 0):
        return False

    q = """UPDATE sites
    SET shared = ?
    WHERE id = ?"""

    if (r[0][0] == 0): # used to be private, now becomes public
        c.execute(q, (1, id))
    else: # used to be public, now becomes private
        c.execute(q, (0, id))

    conn.commit()

    return True

def fork_shared_site(site_id, email):
    """
    fork_shared_site: this makes a copy of the shared site with a specific
    site_id within the user's private library

    Args:
        site_id (int): the site_id of the shared site
	email (string): the user who wishes to fork the site
    
    Returns:
        The new ID of the forked site, or -1 if unsuccessful
    """

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.shared, sites.title, sites.site, sites.comments, sites.notes
    FROM sites
    WHERE sites.id = ?"""

    r = c.execute(q, (site_id,)).fetchall()

    if (len(r) == 0):
        return -1

    if r[0][0] == 0:
        return -1

    return add_to_sites(email, r[0][1], r[0][2], r[0][3], r[0][4])

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

def search_user_sites(email, search_string):
    """
    search_user_sites: searches a specific user's pages for a specific set of
    strings

    Args:
        email (string): the user
	search_string (string): the string to search
    
    Returns:
        a list of abstracted articles in which each element is a dictionary of
        the form:
        {
            'index' : index-of-proximity (see search.py) (float),
            'id' : site id (int),
            'abstract' : abstracted site (string),
            'snippet' : list of matched words (see search.py)
        }

        ordered by 'index'
    """

    ret_val = []
    search = search_string.split()

    conn = sqlite3.connect("./db/infos.db")
    c = conn.cursor()

    q = """SELECT sites.id, sites.site, sites.title, sites.comments, sites.notes
    FROM sites WHERE sites.email = ?"""

    result = c.execute(q, (email,)).fetchall()

    for i in result:
        soup = BeautifulSoup(i[1] + i[3])
        site_cleaned = i[2] + ' ' + soup.get_text() + i[4]
        snippets = get_snippets_from_site(site_cleaned, search)

        if (len(snippets) > 0):
            index = get_index_of_proximity(site_cleaned, search)
            abstract = abstract_site_from_words(site_cleaned, snippets)

            ret_val.append({
                'index':index,
                'id':i[0],
                'abstract':abstract,
                'snippet':snippets,
                'title':i[2]
                })
    
    return sorted(ret_val, key=lambda entry: entry['index'], reverse=True)

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

    print "searching"
    search_user_sites("alex.wyc2098@gmail.com", 'asdf')
