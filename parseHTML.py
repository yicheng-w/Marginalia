#################################################################################
# Parse HTML for the project, handles the BeautifulSoup and HTML that is passed #
#                                                                               #
# Authors                                                                       #
#  Jeffrey Zou                                                                  #
#                                                                               #
# Description                                                                   #
#  Handles the formatting of the HTML                                           #
#                                                                               #
#################################################################################

from bs4 import BeautifulSoup
#import urllib2

def pretty():
    thePage = '''
    <html>
    <body>
    <p>Hi</p>
    </body>
    </html>
    '''

    soup = BeautifulSoup(thePage, "html.parser")
    print soup.get_text()
