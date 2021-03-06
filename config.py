import jinja2
from flask import Flask,request,jsonify,Blueprint
import json
import sqlite3
import base64
import hashlib

app = Flask(__name__,static_url_path="")
app.config.update(DEBUG=True)
from views.public import *
from views.api import *
app.register_blueprint(public, url_prefix="")
app.register_blueprint(api, url_prefix="/api")

@app.errorhandler(404)
def page_not_found(error):
    return app.send_static_file("html/404.html"),404
