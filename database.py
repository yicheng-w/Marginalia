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

from pymongo import MongoClient
from time import time, sleep
from search import *
from bs4 import BeautifulSoup

class DBManager:
    """
    Class to manage the annotation database
    """

    def __init__(self, user_db_name, sites_db_name):
        self.conn = MongoClient()
        self.user_db = conn[user_db_name]
        self.sites_db = conn[sites_db_name]

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
            >>> new_user("alex.wyc2098@gmail.com", "7b77e4d3de87423f0c98716ad54bd2f3", "Yicheng", "Wang")
            True
            >>> new_user("alex.wyc2098@gmail.com", "12354ab6a7e87af879dbadf87124faab", "Yicheng", "Wang")
            False (because the email has already been registered)
        """
        
        ps = list(self.user_db.find({'email':email}))

        if ps == []:
            user = {'email': email,
                    'password': password_hash,
                    'first': first,
                    'last': last}
            self.user_db.insert(user)
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
            >>> authenticate("alex.wyc2098@gmail.com", "7b77e4d3de87423f0c98716ad54bd2f3")
            True
            >>> authenticate("alex.wyc2098@gmail.com", "12354ab6a7e87af879dbadf87124faab")
            False    
        """

        result = list(self.user_db.find({'email':email, 'password':password_hash}))

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

        return self.user_db.update(
                {"email": email},
                {
                    '$set':
                        {
                            'password': new_password
                        }
                    }
                )['n'] == 1


