#! coding:utf-8
# 使用sqlite数据库
from flask import Flask
import sqlite3
from contextlib import closing
from flask import Flask, redirect
from flask import request
from flask import jsonify
from token.py import generate_token

app = Flask(__name__)

app.config.update(
    DATABASE = 'user.db',      #相对于文件所在目录
    DEBUG=True,
)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = connect_db()
    cur = db.cursor()
    return db, cur

def send_json(num,token):
    info = dict()
    if num == 1:
        info['success'] = "1"
        info['token'] = token
        info['msg'] = "登录成功~"
        jsonify(info)           #发送至前端
    if num == 0:
        token = ""
        info['msg'] = "登录失败~"
        info['success'] = "0"
        jsonify(info)   #发送至前端


#登录
@app.route('/api/login', methods=['POST', 'GET'])
def login():
    token = ""
    try:
        if request.method == 'POST':

            username = request.form['username']
            password = request.form['password']
            db, cur = get_db()

            passwd_hash_tuple = cur.execute(
                'SELECT password FROM users WHERE username=?', [username]).fetchone()   # return a tuple

            if not passwd_hash_tuple:
                send_json(0,token)
            elif password!= passwd_hash_tuple[0]:
                send_json(0,token)
            else:
                token, ts_str = generate_token(username,password)
                cur.execute("UPDATE user SET token=? WHERE username=?", [token,username])
                send_json(1,token)
    except:
        send_json(0,token)
    db.commit()
    cur.close()
    db.close()