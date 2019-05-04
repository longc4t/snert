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
        self.user.addarticle(articleid=articleid,userid=articleauthorid)
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
        articlevalue = self.cur.select(field=("*"), tablename="article", selectkey="articleid", selectvalue=articleid)[0]
        return jsonify({"success": 1, "data": {
            "articleid": articlevalue[0],
            "articletitle": articlevalue[1],
            "articleauthor": articlevalue[2],
            "articleauthorid": articlevalue[3],
            "articlecontent": articlevalue[4],
            "articletimestamp": articlevalue[5],
            "commentid": articlevalue[6],
        }})

    def getcomment(self,articleid):
        comment = self.cur.select(
            field=("commentid"), tablename="article", selectkey="articleid",
            selectvalue=articleid)[0]
        return comment

    def addcomment(self, commentid, articleid):
        comment = eval(self.getcomment(articleid=articleid))
        comment.append(commentid)
        self.cur.update(tablename="article", keymap={"commentid", str(comment)}, updatekey="articleid",
                        updatevalue=articleid)
