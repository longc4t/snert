from flask import Flask,request,jsonify,Blueprint
import re
import requests
import socket
import json
import sqlite3
import pymysql
import base64
import hashlib
app = Flask(__name__,static_url_path="")
app.config.update(DEBUG=True)
from views.user import *
from views.api import *
app.register_blueprint(user, url_prefix="")
app.register_blueprint(api, url_prefix="/api")


#token 鉴权
def certify_token(username, password, token):
    key = "{0}|{1}".format(username, password)
    b64_key = base64.b64encode(key.encode("utf-8"))
    new_token = hashlib.md5(b64_key).hexdigest()
    if token != new_token:
        # token certification failed
        return False
    # token certification success
    return True
