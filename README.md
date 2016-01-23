# Marginalia

"Marginalia," or marginal notes in Latin, is an application that lets people
annotate articles online.

## Project Description

###Summary
This is a chrome extension used to annotate articles. There are many extensions
and webapps that allows people to take notes on articles, however, almost none
of them allows for annotation. With this extension, you can freely markup the
text as well as take general notes on a side panel.

###Features:

- Reformats articles in ad-free, easy to read manner

- Allows users highlight/comment on the article

- Allows users to take general note on the side

- Allows users to save their annotated article in an account on the cloud

- Allows users to get a permlink of their annotated article to share with the
   world

- Allows users to search for keywords in their sites

###Features For Future Development

- Save a user's articles locally so one can read/comment offline

- Allowing users to use Marginalia on pdf's

- Add an abstraction/summarization tool that compiles a summary of the article
   based on the highlighted/commented text

- Add formatting to comments and notes

- Exporting the document to pdf or to print

###Toolset

The login/user data system is written in sqlite3 and python

The front end is written with the help of [Materialize CSS](http://materializecss.com/)

The javascript is written with the help of Materialize and jQuery

###Demo

TODO

## Files and Folders

api.py/api-gunicorn.py - The main server file, powered by flask

database.py - The database management program, powered by python and sqlite3

search.py - The search engine used by the program, written in python

init.py - Builds and initializes the database

restart.sh - Wipes the database and creates a new one, also starts the server
with green unicorn in the background

db/ - The folder that houses the database, which will be created by init.py

extension/ - The folder for the unpacked extension

## Project Members

**Leader** - Yicheng Wang  
**Frontend** - Ariel Levy  
**Middleware & Backend** - Jeffrey Zou, Alice Xue
