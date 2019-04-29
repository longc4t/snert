# -*- coding: utf-8 -*-
from config import Blueprint,json,request,app

user = Blueprint('user', __name__)

def getjson():
    return json.loads(request.get_data().decode("utf-8"))


@user.route("/")
@user.route("/index.html")
def indexpage():
    return app.send_static_file("html/index.html")


@user.route("/about")
@user.route("/about.html")
def aboutpage():
    return app.send_static_file("html/about.html")


@user.route("/comment")
@user.route("/comment.html")
def commentpage():
    return app.send_static_file("html/comment.html")


@user.route("/message")
@user.route("/message.html")
def messagepage():
    return app.send_static_file("html/message.html")


@user.route("/details")
@user.route("/details.html")
def detailspage():
    return app.send_static_file("html/details.html")


@user.route("/login")
@user.route("/login.html")
def loginpage():
    return app.send_static_file("html/login.html")
