from conn import sqlop
from .user import user
from config import jsonify, base64, hashlib


class comment(object):
    def __init__(self):
        self.cur = sqlop()
        self.user = user()

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
        self.user.addcomment(commentid=commentid, userid=commentauthorid)


    def getcomment(self, commentarray):
        tmpdata = []
        for i in commentarray:
            commentdata = self.cur.select(field=("*"), tablename="comment", selectkey="commentid", selectvalue=i)[0]
            if commentdata:
                tmpdata.append(
                    {"commentid": commentdata[0], "commentauthor": commentdata[1], "commentauthorid": commentdata[2],
                     "commentcontent": commentdata[3], "commenttimestamp": commentdata[4]})
        return tmpdata


