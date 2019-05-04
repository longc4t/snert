from conn import sqlop
from .user import user
from .article import article
from config import jsonify, base64, hashlib


class comment(object):
    def __init__(self):
        self.cur = sqlop()
        self.user = user()
        self.article = article()

    def getcommentid(self, commentauthor, commenttimestamp):
        key = "{0}|{1}".format(commentauthor, commenttimestamp)
        b64_key = base64.b64encode(key.encode("utf-8"))
        commentid = hashlib.md5(b64_key).hexdigest()
        return commentid

    def insertcomment(self, commentauthor, commentcontent, commenttimestamp):
        commentid = self.getcommentid(commentauthor=commentauthor, commenttimestamp=commenttimestamp)
        commentauthorid = self.user.getuserid(username=commentauthor)
        self.cur.insert(tablename="comment",
                        insertvalue=(commentid, commentauthor, commentauthorid, commentcontent, commenttimestamp))

        return jsonify({"success": 1, "msg": "添加成功"})

    def getcomment(self):
        commentdata = self.cur.showcomment()
        jsonformatstring = {"success": 1, "count": len(commentdata), "data": []}
        for i in commentdata:
            jsonformatstring["data"].append({"commentid": i[0], "commentauthor": i[1], "commentauthorid": i[2],
                                             "commentcontent": i[3], "commenttimestamp": i[4]})
        return jsonify(jsonformatstring)
