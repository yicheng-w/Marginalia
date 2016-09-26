################################################################################
# Backend                                                                      #
# database management for Mawrginalia, backed by MongoDB                       #
#                                                                              #
# Authors                                                                      #
#  Yicheng                                                                     #
#  Wang                                                                        #
#                                                                              #
# Description                                                                  #
#  Deals                                                                       #
#  with database in various fashions, using MongoDB                            #
#                                                                              #
################################################################################

# TODO
#  TODO-List

# Dev Log
#  Project Created: 2016-08-21 15:41 - Yicheng W.

from time import time, sleep
from search import *
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
import pymongo

class DBManager:
    """
    Class to manage the annotation database
    """

    def __init__(self, database_name, user_collection_name, site_collection_name):
        self.client = pymongo.MongoClient()
        self.db = self.client[database_name]
        self.user_collection = self.db[user_collection_name]
        self.site_collection = self.db[site_collection_name]

    # {{{ User Functions
    def new_user(self, email, password_hash, first, last):
        """
        new_user: adds a new user to the database, returns False if
        unsuccessful
    
        Args:
            email (string): email of the new user
            password_hash (string): hex string of a hashed password
            first (string): the first name of the user
            last (string): the last name of the user
        
        Returns:
            True if successfully added, False otherwise (email has already been
            taken)
        
        Example:
            >>> new_user("test@email.com", "7b77e4d3de87423f0c98716ad54bd2f3", "Yicheng", "Wang")
            True
            >>> new_user("test@email.com", "12354ab6a7e87af879dbadf87124faab", "Yicheng", "Wang")
            False (because the email has already been registered)
        """
        
        ps = list(self.user_collection.find({'email':email}))

        if ps == []:
            user = {'email': email,
                    'password': password_hash,
                    'first': first,
                    'last': last}
            self.user_collection.insert(user)
            return True

        else:
            return False

    def authenticate(self, email, password_hash):
        """
        authenticate: authenticates an user login

        Args:
            email (string): the email to authenticate
            password_hash (string): the hash of the password that the user inputed
        
        Returns:
            True if the two match, False otherwise
        
        Example:
            >>> authenticate("test@email.com", "7b77e4d3de87423f0c98716ad54bd2f3")
            True
            >>> authenticate("test@email.com", "12354ab6a7e87af879dbadf87124faab")
            False    
        """

        result = list(self.user_collection.find({'email':email, 'password':password_hash}))

        return (len(result) != 0)

    def update_pwd(self, email, new_password):
        """
        update_pwd: updates password for an user

        Args:
            email (string): the user
            new_password (string): the new password
        
        Returns:
            True if successful, False otherwise
        """

        return self.user_collection.update_one(
                {"email": email},
                {
                    '$set':
                        {
                            'password': new_password
                        }
                    }
                ).matched_count == 1

    def get_name_from_email(self, email):
        """
        get_name_from_email: returns the name of the client based on the email
        entered

        Args:
            email (string): the email you are looking for
        
        Returns:
            a string of the form "first last", empty string if the email doesn't
            exist
        
        Example:
            get_name_from_email("test@email.com") --> Yicheng Wang    
        """

        if self.user_collection.count({'email':email}) != 1:
            return ""

        res = self.user_collection.find_one({'email': email})

        return res['first'] + ' ' + res['last']

    # }}}
    # {{{ Sites Functions
    def add_to_sites(self, email, title, site, comments = "", notes = ""):
        """
        add_to_sites: add a site to the user's list

        Args:
            email (string): the user
            title (string): title of the site
            site (string): the html source code of the site
            comments (string): the comments on the site (default to empty string)
            notes (string): the notes on the site (default to empty string)
        
        Returns:
            the id of the new site if successful, -1 otherwise
        """

        if self.user_collection.count({"email": email}) != 1: # possible js/package sniffed atk
            return -1

        res = self.site_collection.insert_one(
                    {
                        'email': email,
                        'title': title,
                        'site': site,
                        'comments': comments,
                        'notes': notes,
                        'shared': False,
                        'last_edited': time()
                    }
                )

        return res.inserted_id

    def get_list_of_sites(self, email):
        """
        get_list_of_sites: returns a list of sites based on a certain email

        Args:
            email (string): the user
        
        Returns:
            a list of sites in dictionary format ranked by last edited
            time:
                [{
                    'email': email,
                    'title': title,
                    'site': site,
                    'comments': comments,
                    'notes': notes,
                    'shared': False,
                    'last_edited': time(),
                    '_id': ObjectId('hex string')
                }, ...]
        """

        r = self.site_collection.find({
            'email': email
            }).sort("last_edited", pymongo.DESCENDING)

        return list(r)

    def get_site_on_id(self, email, id):
        """
        get_site_on_id: get the site title, site, the notes and the comments

        Args:
            email (string): the user
            id (string): the site id
        
        Returns:
            the site dictionary, as outlined by previous functions,
            or none if retrival was not successful
        """

        return self.site_collection.find_one({
            '_id': ObjectId(id),
            'email': email
            })

    def update_site(self, email, site_id, new_site, new_comments, new_notes):
        """
        update_site: updates the site entry for the user

        Args:
            email (string): the user
            site_id (string): the ObjectId of the site in the database
            new_site (string): updated markup for the site
            new_comments (string): updated comments for the site
            new_notes (string): updated notes for the site
        
        Returns:
            True if successful, False otherwise    
        """

        return self.site_collection.update_one(
                {
                    '_id': ObjectId(site_id),
                    'email': email
                },
                {
                    '$set': {
                        'site': new_site,
                        'comments': new_comments,
                        'notes': new_notes,
                        'last_edited': time()
                    }
                }
            ).matched_count == 1

    def delete_site(self, email, site_id):
        """
        delete_site: deletes a site from the user's "library" according to id

        Args:
            email (string): the user
            site_id (string): id of the site
        
        Returns:
            True if successful, False otherwise
        """
        return self.site_collection.find_one_and_delete(
                    {
                        '_id': ObjectId(site_id),
                        'email': email
                    }
                ) != None

    def change_site_permission(self, email, id):
        """
        change_site_permission: changes the permission of a site (public -> private
        or private -> public)

        Args:
            email (string): the user
            id (string): the id of the site
        
        Returns:
            True if successful, False if the id and the email doesn't match
        """

        doc = self.site_collection.find_one(
                    {
                        '_id': ObjectId(id),
                        'email': email
                    }
                )

        if doc:
            return self.site_collection.update_one(
                        {
                            '_id': ObjectId(id),
                            'email': email
                        },
                        {
                            '$set': {'shared': not doc['shared']}
                        }
                    ).matched_count == 1

        else:
            return False

    def get_site_for_sharing(self, id):
        """
        get_site_for_sharing: get the content of one site for sharing, returns None
        if the site doesn't exist or is private

        Args:
            id (string): the ID of the site
        
        Returns:
            the site dictionary or none if retrival was not successful
        """

        return self.site_collection.find_one(
                    {
                        '_id': ObjectId(id),
                        'shared': True
                    }
                )

    def fork_shared_site(self, site_id, email):
        """
        fork_shared_site: this makes a copy of the shared site with a specific
        site_id within the user's private library

        Args:
            site_id (string): the site_id of the shared site
            email (string): the user who wishes to fork the site
        
        Returns:
            The new ID of the forked site, or -1 if unsuccessful
        """

        res = self.site_collection.find_one(
                    {
                        '_id': ObjectId(site_id),
                        'shared': True
                    }
                )

        if res:
            return self.add_to_sites(email, res['title'], res['site'], res['comments'], res['notes'])

        return -1

    # }}}

if __name__ == "__main__":
    Test = DBManager('test_db', 'test_user_collection', 'test_site_collection')
    print "new_user test"
    print Test.new_user("test@email.com", "12345", "Yicheng", "Wang")
    print Test.new_user("test@email.com", "dgjsadkfhsa", "Yicheng", "Wang")
    print Test.new_user("test2@email.com", "ajdfsadfk", "Yicheng", "Wang")

    print "\nauthentication test"
    print Test.authenticate("test@email.com", "12345")
    print Test.authenticate("test2@email.com", "12345")
    print Test.authenticate("asdf@asdf.asdf", "12435")

    print "\nchange password test"
    print Test.update_pwd("test@email.com", "54321")
    print Test.update_pwd("asdf@asdf.com", "12345")

    print Test.authenticate("test@email.com", "12345")
    print Test.authenticate("test@email.com", "54321")

    print "\nget name test"
    print Test.get_name_from_email("test@email.com")
    print Test.get_name_from_email('test2@email.com')
    print Test.get_name_from_email("noemail@lol.com")

    print "\nadd to sites test"
    email = "test@email.com"
    id = Test.add_to_sites(email, "123456789", "url_lol")
    print id
    print Test.add_to_sites("test2@email.com", "fkjhsadgfkvasv", "url_lol")
    id2 = Test.add_to_sites(email, "12hsadffghas", "url_lol")
    print id2
    print Test.add_to_sites("noemail", "asdjfkh", "asdjkf")

    print Test.get_list_of_sites(email)
    print Test.get_list_of_sites("test2@email.com")

    print "\nget site on id test"
    print Test.get_site_on_id(email, id)
    print Test.get_site_on_id('noemail', id)

    print "\nupdate site test"
    print Test.update_site('wrongemail@gmail.com', id, "no, html", "hello", "more stuff")
    print Test.update_site(email, id, "no, html", "hello", "more stuff")
    print Test.get_site_on_id(email, id)

    print "\nchange permission test and get site for sharing"
    print Test.change_site_permission("lol", id)
    print Test.change_site_permission(email, id)
    print Test.get_site_on_id(email, id)
    print Test.get_site_for_sharing(id)
    print Test.change_site_permission(email, id)
    print Test.get_site_on_id(email, id)
    print Test.get_site_for_sharing(id)

    print "\ndelete site test"
    print Test.delete_site("noemail", id2)
    print Test.delete_site(email, id2)
    print Test.get_list_of_sites(email)

    Test.user_collection.remove()
    Test.site_collection.remove()
