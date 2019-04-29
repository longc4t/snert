from flask import Flask,request,jsonify,Blueprint
import re
import requests
import socket
import json
app = Flask(__name__,static_url_path="")
app.config.update(DEBUG=True)
from views.user import *
from views.api import *
app.register_blueprint(user, url_prefix="")
app.register_blueprint(api, url_prefix="/api")

