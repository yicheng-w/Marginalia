# Marginalia

"Marginalia," or marginal notes in Latin, is an application that lets people
annotate articles online.

The main site is up and running [here](http://marginalia.alex-wyc.me:8000), and the
chrome extension is "extension.crx"

## Project Description

###Summary
This is a chrome extension used to annotate articles. There are many extensions
and webapps that allow people to take notes on articles. However, almost none
of them allow for annotation. With this extension, you can freely markup the
text as well as take general notes on a side panel. For more information, click
[here](http://marginalia.alex-wyc.me:8000/about).
To watch a demo video, click [here](https://www.youtube.com/watch?v=OBCynq96As0&feature=youtu.be)

###Features:

- Reformats articles in an ad-free, easy to read manner

- Allows users to highlight/comment on the article

- Allows users to take general notes on the side

- Allows users to save their annotated article in an account on the cloud

- Allows users to get a permlink of their annotated article to share with the
   world

- Allows users to search for keywords in their sites

###Features For Future Development:

- Save a user's articles locally so one can read/comment offline

- Allow users to use Marginalia on pdf's

- Add an abstraction/summarization tool that compiles a summary of the article
   based on the highlighted/commented text

- Add formatting to comments and notes

- Export the document to pdf or to print
 
- Allow users to organize articles into folders
 
- Incorporate pictures from webpages into the saved articles in Marginalia

- Develop bibliography cites for a user's articles

###Toolset:

The login/user data system is written in sqlite3 and python

The front end is written with the help of [Materialize CSS](http://materializecss.com/)

The javascript is written with the help of Materialize and jQuery

## Files and Folders:

api.py - The main server file, powered by flask

database.py - The database management program, powered by python and sqlite3

search.py - The search engine used by the program, written in python

init.py - Builds and initializes the database

restart.sh - Wipes the database and creates a new one, also starts the server
with green unicorn in the background

extension.crx - packed chrome extension

db/ - The folder that houses the database, which will be created by init.py

extension/ - The folder for the unpacked extension

## Project Members:

**Leader** - Yicheng Wang  
**Frontend** - Ariel Levy  
**Middleware & Backend** - Jeffrey Zou, Alice Xue
