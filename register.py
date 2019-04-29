#! coding:utf-8
# 使用sqlite数据库
from flask import Flask
import sqlite3
from contextlib import closing
from flask import Flask
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
        info['msg'] = "注册成功~"
        jsonify(info)           #发送至前端
    if num == 0:
        token = ""
        info['msg'] = "用户名已占用~"
        info['success'] = "0"
        jsonify(info)   #发送至前端
    if num == -1:
        token = ""
        info['msg'] = "注册失败~"
        info['success'] = "0"
        jsonify(info)  # 发送至前端

#注册
@app.route('/api/reg', methods=['POST','GET'])
def register():
    token = ""
    try:
        if request.methods == 'POST':
            username = request.form['username']
            password = request.form['password']

            db, cur = get_db()

            x = cur.execute(
                'SELECT * FROM users WHERE username = ?', [username])

            if x.fetchall():
                send_json(0,token)
            else:
                token,ts_str = generate_token(username,password)
                personsay = "这个家伙很懒，什么也没留下~"
                cur.execute("INSERT INTO users (username, password，token,personsay) VALUES(?,?,?,?)", [
                            username, password,token,personsay])
                send_json(1, token)
    except:
        send_json(-1,token)
    db.commit()
    cur.close()
    db.close()
