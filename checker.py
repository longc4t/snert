# -*- coding:utf8 -*-
import sys
import random
import requests
import time

global token
global username
mapa = "abcdefghijklmnopqrstuvwxyz"


def check1(url):
    try:
        global username, token
        loginpage = "{domain}{path}".format(domain=url, path="/login")
        register = "{domain}{path}".format(domain=url, path="/api/register")
        checklogin = "{domain}{path}".format(domain=url, path="/api/checklogin")
        username = ''.join(random.sample(mapa, 9))
        pagestatus = True if "register-form" in requests.get(loginpage, timeout=3).text else False

        data = requests.post(register, json={"username": username, "password": "justforfun"}, timeout=3).json()
        registerstatus = True if data["success"] else False
        token = data["token"]
        loginstatus = True if requests.post(checklogin, json={"token": token}, timeout=3).json()["success"] else False

        if pagestatus and registerstatus and loginstatus:
            return True
        else:
            print(
                "page err" if not pagestatus else "register err" if not registerstatus else "login err" if not loginstatus else False)
            return False
    except Exception as e:
        print("checker 1 err")
    return False


def check2(url):
    try:
        global username, token
        addarticle = "{domain}{path}".format(domain=url, path="/api/article/add")
        data = requests.post(addarticle, json={"articletitle": "Y2hlY2t0ZXN0", "articleauthor": username,
                                               "articlecontent": "Y2hlY2t0ZXN0",
                                               "articletimestamp": str(int(time.time() * 1000)),
                                               "token": token}, timeout=3).json()
        return True if data["success"] else False
    except Exception as e:
        print("checker 3 err")
    return True


def check3(url):
    try:
        global username, token
        commentpage = "{domain}{path}".format(domain=url, path="/api/comment/add")
        data = requests.post(commentpage, json={"commentcontent": "Y2hlY2t0ZXN0", "commentauthor": username,
                                                "commenttimestamp": str(int(time.time() * 1000)),
                                                "token": token}, timeout=3).json()
        return True if data["success"] else False
    except Exception as e:
        print("checker 3 err")
    return True


def checker(host, port):
    try:
        url = "http://" + host + ":" + str(port)
        if check1(url) and check2(url) and check3(url):
            return (True, "IP: " + host + " OK")
    except Exception as e:
        return (False, "IP: " + host + " is down, " + str(e))


if __name__ == '__main__':
    print(checker("127.0.0.1", 5000))
    # ip=sys.argv[1]
    # port=int(sys.argv[2])
    # print(checker(ip,port))
