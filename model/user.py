from conn import sqlop
from config import jsonify, base64, hashlib


class user(object):
    def __init__(self):
        self.cur = sqlop()

    def isusernameused(self, username):  # check username is ever used
        return 1 if self.cur.select(field=("*"), tablename="user", selectkey="username", selectvalue=username) else 0

    def islogin(self, token):  # check token
        return 1 if self.cur.select(field=("*"), tablename="user", selectkey="token", selectvalue=token) else 0

    def register(self, username, password):
        if self.isusernameused(username):
            return jsonify({"success": 0, "msg": "用户名已被占用~"})
        else:
            userid = self.getuserid(username)
            token = self.generate_token(username, password)
            self.cur.insert(tablename="user",
                            insertvalue=(userid, username, password, token, "6L+Z5piv5Liq5oCn562+5ZCN", "[]", "[]"))
            return jsonify({"success": 1, "msg": "注册成功~", "token": token})

    def login(self, username, password):
        value = self.cur.select(field=("*"), tablename="user", selectkey="username", selectvalue=username)
        print(value)
        if len(value) > 0:
            if password in value[0]:
                return jsonify({"success": 1, "msg": "登录成功～", "token": value[0][3]})
            else:
                return jsonify({"success": 0, "msg": "登录失败～"})
        else:
            return jsonify({"success": 0, "msg": "未找到该账户，请先注册!"})

    def generate_token(self, username, password):
        key = "{0}|{1}".format(username, password)
        b64_key = base64.b64encode(key.encode("utf-8"))
        token = hashlib.md5(b64_key).hexdigest()
        return token

    def getuserid(self, username):
        b64_key = base64.b64encode(username.encode("utf-8"))
        userid = hashlib.md5(b64_key).hexdigest()
        return userid

    def addarticle(self, articleid, userid):
        userarticle = eval(self.getuserarticle(userid=userid))
        userarticle.append(articleid)
        self.cur.update(tablename="user", keymap={"userarticle", str(userarticle)}, updatekey="userid",
                        updatevalue=userid)

    def addcomment(self, commentid, userid):
        usercomment = eval(self.getusercomment(userid=userid))
        usercomment.append(commentid)
        self.cur.update(tablename="user", keymap={"usercomment", str(usercomment)}, updatekey="userid",
                        updatevalue=userid)


    def getuserinfobyid(self, userid):
        username, personsay, article, comment = self.cur.select(
            field=("username", "personsay", "userarticle", "usercomment"), tablename="user", selectkey="userid",
            selectvalue=userid)[0]
        return jsonify(
            {"success": 1, "username": username, "personsay": personsay, "articleid": article, "commentid": comment})

    def getuserarticle(self, userid):
        article = self.cur.select(
            field=("userarticle"), tablename="user", selectkey="userid",
            selectvalue=userid)[0]
        return article

    def getusercomment(self, userid):
        comment = self.cur.select(
            field=("usercomment"), tablename="user", selectkey="userid",
            selectvalue=userid)[0]
        return comment

    def getuserinfobytoken(self, token):
        username, personsay, article, comment = self.cur.select(
            field=('username', 'personsay', 'userarticle', 'usercomment'), tablename="user", selectkey="token",
            selectvalue=token)[0]
        return jsonify(
            {"success": 1, "username": username, "personsay": personsay, "articleid": article, "commentid": comment})

    def updateinformation(self, oldpassword, newpassword, personsay, oldtoken):
        username, password = \
            self.cur.select(field=("username", "password"), tablename="user", selectkey="token",
                            selectvalue=oldtoken)[0]

        if password == oldpassword:
            newtoken = self.generate_token(username=username, password=newpassword)
            self.cur.update(tablename="user",
                            keymap={"password": newpassword, "token": newtoken, "personsay": personsay},
                            updatekey="token",
                            updatevalue=oldtoken
                            )
            return jsonify({"success": 1, "msg": "修改成功", "token": newtoken})
        else:
            return jsonify({"success": 0, "msg": "原密码错误"})
