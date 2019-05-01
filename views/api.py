from config import Blueprint,json,request
from model.user import user
api = Blueprint('api', __name__)


def getjson():
    return json.loads(request.get_data().decode("utf-8"))


@api.route('/login', methods=['POST', 'GET'])
def login():
    userdata = getjson()
    userobj = user()
    return userobj.login(userdata["username"], userdata["password"])


@api.route('/register', methods=['POST'])
def register():
    userdata=getjson()
    userobj=user()
    return userobj.register(userdata["username"],userdata["password"])


'''
#查找评论
@api.route("/comment/search", methods=["POST"])
def searchcomment():
    reqdata = getjson()
    if checklogin(reqdata["token"]):
        returndata = {"success": 1, "data": []}
        db, cur = get_db()
        for i in reqdata["commentidarrary"]:
            sqldata = cur.execute("select * from article where commentid= ?", i)
            tmpdata = dict(sqldata)
            returndata["data"].append(tmpdata)
            db.commit()
            cur.close()
            db.close()
            return jsonify(returndata)
    else:
        return jsonify({"success": 0, "msg": "请登录"})


#添加评论
@api.route("/comment/add", methods=["POST"])
def addcomment():
    reqdata = getjson()
    if checklogin(reqdata["token"]):
        try:
            db, cur = get_db()
            cur.execute("INSERT INTO Persons VALUES (?,?,?,?)", [reqdata["commentauthor"],
                           reqdata["commentauthorid"], reqdata["commentcontent"], reqdata["commenttimestamp"]])
            db.commit()
            cur.close()
            db.close()
            return jsonify({"success": 1, "msg": "添加成功"})
        except:
            db.commit()
            cur.close()
            db.close()
            return jsonify({"success": 0, "msg": "添加失败"})

    else:
        return jsonify({"success": 0, "msg": "请登录"})


# 添加文章
@api.route("/article/add",methods=["POST"])
def send_article():
    reqdata=getjson()
    if checklogin(reqdata["token"]):
        db, cur = get_db()
        try:
            cur.execute("INSERT INTO Persons VALUES (?, ?, ?, ?)",[reqdata["article_author"],reqdata["article_authorid"], reqdata["article_content"], reqdata["article_timestamp"]])
            db.commit()
            cur.close()
            db.close()
            return jsonify({"success": 1, "msg": "发送成功"})

        except:
            db.commit()
            cur.close()
            db.close()
            return jsonify({"success": 0, "msg": "发送失败"})

    else:
        return jsonify({"success": 0, "msg": "请登录"})

# 搜索文章
@api.route("/article/search",methods=["POST"])
def articlesearch():
    reqdata=getjson()
    if checklogin(reqdata["token"]):
        returndata={"success":1,"data":[]}
        db, cur = get_db()
        for i in reqdata["articleidarray"]:
            sqldata = cur.execute("select * from article where articleid= ?",i)
            tmpdata=dict(sqldata)
            returndata["data"].append(tmpdata)
        db.commit()
        cur.close()
        db.close()
        return jsonify(returndata)
    else:
        return jsonify({"success":0,"msg":"请登录"})

# 文章分页显示
@api.route("/article/index",methods=["POST"])
def articleshow():
    reqdata=getjson()
    db, cur = get_db()
    if checklogin(reqdata["token"]):
        returndata={"success":1,"data":[]}
        for i in reqdata["articleidarray"]:
            sqldata = cur.execute("select * from article desc articletimestamp limit ?,?",[i,i*3+3])
            tmpdata=dict(sqldata)
            returndata["data"].append(tmpdata)
        return jsonify(returndata)
    else:
        return jsonify({"success":0,"msg":"请登录"})

#修改个人信息
@api.route("/user/change",methods=["POST"])
def change():
    reqdata = getjson()
    if checklogin(reqdata["token"]):
        db, cur = get_db()
        cursor = cur.execute("SELECT personsay,username,password,token FROM user WHERE userid= ?", reqdata['userid'])
        users = dict(cursor)
        if (not reqdata['oldpassword'] or not reqdata['newpassword']):
            token = generate_token(users['username'], reqdata['newpassword'])
            cur.execute("UPDATE user SET personsay=? WHERE userid=?", reqdata['personsay'], reqdata['userid'])
            cur.execute("UPDATE user SET token=? WHERE userid=?", token, reqdata['userid'])
            db.commit()
            cur.close()
            db.close()
            return jsonify({"success": 1, "token": users['token'], "msg": "修改成功"})
        elif reqdata['oldpassword'] != users['password']:
            token = generate_token(users['username'], reqdata['newpassword'])
            cur.execute("UPDATE user SET password=? WHERE userid=?", reqdata['newpassword'], reqdata['userid'])
            cur.execute("UPDATE user SET personsay=? WHERE userid=?", reqdata['personsay'], reqdata['userid'])
            cur.execute("UPDATE user SET token=? WHERE userid=?", token, reqdata['userid'])
            db.commit()
            cur.close()
            db.close()
            return jsonify({"success": 1, "token": token, "msg": "修改成功"})
        else:
            db.commit()
            cur.close()
            db.close()
            return jsonify({"success": 0, "token": "", "msg": "密码不正确"})
    else:
        return jsonify({"success": 0, "token": "", "msg": "鉴权失败"})

'''