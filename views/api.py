from config import Blueprint,json,request,base64,hashlib,jsonify,sqlite3,app
api = Blueprint('api', __name__)


def getjson():
    return json.loads(request.get_data().decode("utf-8"))

@api.route("/")
@api.route("/testapi")
def testapi():
    return "<h1>TEST API!"

#生成token
def generate_token(username, password):
    key = "{0}|{1}".format(username, password)
    b64_key = base64.b64encode(key.encode("utf-8"))
    token = hashlib.md5(b64_key).hexdigest()
    return token


#连接数据库
def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    cur = db.cursor()
    return db, cur


#装饰器
def checklogin(token):
    cur, cursor = get_db()
    tokens = cursor.fetchall()
    cursor.close()
    cur.close()
    for i in tokens:
        if token == i:
            # Already logged in
            return True
        else:
            pass
    # Not logged in
    return False

#发送json数据至前端
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

        
        
#登录
@api.route('/login', methods=['POST', 'GET'])
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
                token = generate_token(username,password)
                cur.execute("UPDATE user SET token=? WHERE username=?", [token,username])
                send_json(1,token)
    except:
        send_json(0,token)
    db.commit()
    cur.close()
    db.close()
    
    
#注册
@api.route('/reg', methods=['POST','GET'])
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
                token = generate_token(username,password)
                personsay = "这个家伙很懒，什么也没留下~"
                cur.execute("INSERT INTO users (username, password，token,personsay) VALUES(?,?,?,?)", [
                            username, password,token,personsay])
                send_json(1, token)
    except:
        send_json(-1,token)
    db.commit()
    cur.close()
    db.close()


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
            cur.execute("INSERT INTO Persons VALUES (?, ?, ?, ?)", reqdata["commentauthor"],
                           reqdata["commentauthorid"], reqdata["commentcontent"], reqdata["commenttimestamp"])
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
            cur.execute("INSERT INTO Persons VALUES (?, ?, ?, ?)",reqdata["article_author"],reqdata["article_authorid"], reqdata["article_content"], reqdata["article_timestamp"])
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
            sqldata = cur.execute("(select * from article desc articletimestamp limit ?*3,?*3+3),?",i)
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
