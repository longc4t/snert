# -*- coding: utf-8 -*-
from flask import Flask, render_template, \
    request, jsonify,render_template_string
import json
import base64
import requests
import hashlib
from conn import  *

app = Flask(__name__)


def getjson():
    return json.loads(request.get_data().decode("utf-8"))


@app.route("/")
@app.route("/index.html")
@app.route("/default.html")
def index():
    return render_template("default.html")


