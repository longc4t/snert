# -*- coding: utf-8 -*-
from config import Blueprint,json,request,app

public = Blueprint('public', __name__)

def getjson():
    return json.loads(request.get_data().decode("utf-8"))


@public.route("/")
@public.route("/index.html")
def indexpage():
    return app.send_static_file("html/index.html")


@public.route("/about")
@public.route("/about.html")
def aboutpage():
    return app.send_static_file("html/about.html")


@public.route("/comment")
@public.route("/comment.html")
def commentpage():
    return app.send_static_file("html/comment.html")


@public.route("/message")
@public.route("/message.html")
def messagepage():
    return app.send_static_file("html/message.html")


@public.route("/details")
@public.route("/details.html")
def detailspage():
    return app.send_static_file("html/details.html")


@public.route("/login")
@public.route("/login.html")
def loginpage():
    return app.send_static_file("html/login.html")

@public.route("/user")
@public.route("/user.html")
def userpage():
    return app.send_static_file("html/user.html")
