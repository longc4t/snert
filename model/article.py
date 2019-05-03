from conn import sqlop
from .user import user
from config import jsonify, base64, hashlib


class article(object):
    def __init__(self):
        self.cur = sqlop()
        self.user = user()

    def getarticleid(self, articletitle, articletimestamp):
        key = "{0}|{1}".format(articletitle, articletimestamp)
        b64_key = base64.b64encode(key.encode("utf-8"))
        articleid = hashlib.md5(b64_key).hexdigest()
        return articleid

    def insertarticle(self, articletitle, articleauthor, articlecontent, articletimestamp, commentid="[]"):
        articleid = self.getarticleid(articletitle, articletimestamp)
        articleauthorid = self.user.getuserid(articleauthor)
        self.cur.insert(tablename="article", insertvalue=(
            articleid, articletitle, articleauthor, articleauthorid, articlecontent, articletimestamp, commentid))
        return jsonify({"success": 1, "msg": "添加成功"})

    def getarticle(self):
        data = self.cur.show()
        jsonformatstring = {"success": 1,"count":len(data), "data": []}
        for i in data:
            jsonformatstring["data"].append({"articleid": i[0],
                                             "articletitle": i[1],
                                             "articleauthor": i[2],
                                             "articlecontent": i[4],
                                             "articletimestamp": i[5]
                                             })
        return jsonify(jsonformatstring)

    def getdetail(self, articleid):
        value = self.cur.select(field=("*"), tablename="article", selectkey="articleid", selectvalue=articleid)
        return jsonify({"success": 1, "data": {
            "articleid": value[0],
            "articletitle": value[1],
            "articleauthor": value[2],
            "articleauthorid": value[3],
            "articlecontent": value[4],
            "articletimestamp": value[5],
            "commentid": value[6]
        }})
