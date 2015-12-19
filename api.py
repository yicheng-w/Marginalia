################################################################################
# API for the Annotation project, handles AJAX calls and gives out JSON        #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang                                                                #
#                                                                              #
# Description                                                                  #
#  Handles AJAX calls and database management                                  #
#                                                                              #
################################################################################

# TODO
#  Figure out ajax calls' location and necessity

# Dev Log
#  Project Created: 2015-12-19 14:57 - Yicheng W.

from flask import Flask, request, render_template
from database import *

import json
import requests
from sys import argv

app = Flask(__name__)

@app.route("/")
def root():
    return ""

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, debug = ("--debug" in argv))
