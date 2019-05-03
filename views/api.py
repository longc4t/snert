from config import Blueprint, json, request, jsonify
from model.user import user
from model.article import article

api = Blueprint('api', __name__)


def getjson():
    return json.loads(request.get_data().decode("utf-8"))


@api.route('/login', methods=['POST'])
def login():
    userdata = getjson()
    userobj = user()
    return userobj.login(userdata["username"], userdata["password"])


@api.route('/register', methods=['POST'])
def register():
    userdata = getjson()
    userobj = user()
    return userobj.register(userdata["username"], userdata["password"])


@api.route('/checklogin', methods=['POST'])
def checklogin():
    userdata = getjson()
    userobj = user()
    if userobj.islogin(token=userdata["token"]):
        return jsonify({"success": 1, "msg": "已登录"})
    else:
        return jsonify({"success": 0, "msg": "登录超时"})


'''
#查找评论
@api.route("/comment/search", methods=["POST"])
def searchcomment():
    userdata = getjson()
    if checklogin(userdata["token"]):
        returndata = {"success": 1, "data": []}
        db, cur = get_db()
        for i in userdata["commentidarrary"]:
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
    userdata = getjson()
    if checklogin(userdata["token"]):
        try:
            db, cur = get_db()
            cur.execute("INSERT INTO Persons VALUES (?,?,?,?)", [userdata["commentauthor"],
                           userdata["commentauthorid"], userdata["commentcontent"], userdata["commenttimestamp"]])
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




# 搜索文章
@api.route("/article/search",methods=["POST"])
def articlesearch():
    userdata=getjson()
    if checklogin(userdata["token"]):
        returndata={"success":1,"data":[]}
        db, cur = get_db()
        for i in userdata["articleidarray"]:
            sqldata = cur.execute("select * from article where articleid= ?",i)
            tmpdata=dict(sqldata)
            returndata["data"].append(tmpdata)
        db.commit()
        cur.close()
        db.close()
        return jsonify(returndata)
    else:
        return jsonify({"success":0,"msg":"请登录"})



'''
# 文章分页显示
@api.route("/article/index",methods=["POST"])
def articleshow():
    userdata = getjson()
    articleobj = article()
    userobj = user()
    if userobj.islogin(userdata["token"]):
        return articleobj.getarticle()
    else:
        return jsonify({"success": 0, "token": "", "msg": "登录超时"})


@api.route("/user/change", methods=["POST"])
def change():
    userdata = getjson()
    userobj = user()
    if userobj.islogin(userdata["token"]):
        return userobj.updateinformation(oldpassword=userdata["oldpassword"], newpassword=userdata["newpassword"],
                                         personsay=userdata["personsay"], oldtoken=userdata["token"])
    else:
        return jsonify({"success": 0, "token": "", "msg": "登录超时"})


@api.route("/user/getinfo", methods=["POST"])
def getuserinfo():
    userdata = getjson()
    userobj = user()
    if "userid" in userdata.keys():
        return userobj.getuserinfobyid(userdata["userid"])
    else:
        return userobj.getuserinfobytoken(userdata["token"])


# 添加文章
@api.route("/article/add", methods=["POST"])
def send_article():
    userdata = getjson()
    articleobj = article()
    userobj = user()
    if userobj.islogin(userdata["token"]):
        return articleobj.insertarticle(articletitle=userdata["articletitle"], articleauthor=userdata["articleauthor"],
                                        articlecontent=userdata["articlecontent"],
                                        articletimestamp=userdata["articletimestamp"])
    else:
        return jsonify({"success": 0, "token": "", "msg": "登录超时"})
