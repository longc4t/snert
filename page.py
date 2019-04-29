# -*- coding: utf-8 -*-
from flask import Flask, render_template, \
    request, jsonify,render_template_string
import json
import base64
import requests
import hashlib
from conn import  *

app = Flask(__name__,static_url_path='')

def getjson():
    return json.loads(request.get_data().decode("utf-8"))


@app.route("/")
@app.route("/index.html")
def indexpage():
    return app.send_static_file("html/index.html")


@app.route("/about")
@app.route("/about.html")
def aboutpage():
    return app.send_static_file("html/about.html")

@app.route("/comment")
@app.route("/comment.html")
def commentpage():
    return app.send_static_file("html/comment.html")

@app.route("/message")
@app.route("/message.html")
def messagepage():
    return app.send_static_file("html/message.html")

@app.route("/details")
@app.route("/details.html")
def detailspage():
    return app.send_static_file("html/details.html")


