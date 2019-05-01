from conn import sqlop
from config import jsonify,base64,hashlib

class user(object):
    def __init__(self):
        self.cur=sqlop()

    def isusernameused(self,username):  # check username is ever used
        return 1 if self.cur.select(field=("*"),tablename="user",selectkey="username",selectvalue=username) else 0

    def islogin(self,token): # check token
        return 1 if self.cur.select(field=("*"),tablename="user",selectkey="token",selectvalue=token) else 0

    def register(self,username,password):
        if self.isusernameused(username):
            return jsonify({"success":0,"msg":"用户名已被占用~"})
        else:
            userid=self.getuserid(username)
            token=self.generate_token(username,password)
            self.cur.insert(tablename="user",insertvalue=(userid,username,password,token,"6L+Z5piv5Liq5oCn562+5ZCN","[]","[]"))
            return jsonify({"success":1,"msg":"注册成功~","token":token})

    def login(self,username,password):
        value=self.cur.select(field=("*"),tablename="user",selectvalue=username)
        if password in value:
            return jsonify({"success":1,"msg":"登录成功～"})
        else:
            return jsonify({"success":0,"msg":"登录失败～"})

    def generate_token(self,username, password):
        key = "{0}|{1}".format(username, password)
        b64_key = base64.b64encode(key.encode("utf-8"))
        token = hashlib.md5(b64_key).hexdigest()
        return token

    def getuserid(self,username):
        b64_key = base64.b64encode(username.encode("utf-8"))
        userid = hashlib.md5(b64_key).hexdigest()
        return userid




