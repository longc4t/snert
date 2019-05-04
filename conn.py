import sqlite3


class sqlop:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.sql = ""

    def select(self, field=(), tablename="", selectkey="", selectvalue=""):
        tmpfield = "*" if "*" in field else (field if len(field)<1 else ",".join(field))
        self.sql = "select {field} from {tablename} WHERE {selectkey}= '{selectvalue}'".format(field=tmpfield,
                                                                                               tablename=tablename,
                                                                                               selectkey=selectkey,
                                                                                               selectvalue=selectvalue)
        print(self.sql)
        self.cursor.execute(self.sql)
        values = self.cursor.fetchall()
        return values

    def update(self, tablename="", keymap={}, updatekey="", updatevalue=""):
        setstring = []
        for key,value in keymap.items():
            setstring.append("{key}='{value}'".format(key=key,value=value))
        setstring = ",".join(setstring)
        self.sql = "update {tablename} set {setstring} where {updatekey}='{updatevalue}'".format(tablename=tablename,
                                                                                                 setstring=setstring,
                                                                                                 updatekey=updatekey,
                                                                                                 updatevalue=updatevalue)
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()

    def insert(self, tablename="", insertvalue=()):
        self.sql = "INSERT INTO {tablename} VALUES {insertvalue}".format(tablename=tablename, insertvalue=insertvalue)
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()

    def showarticle(self):
        self.sql = "select * from article order by `articletimestamp` desc"
        print(self.sql)
        self.cursor.execute(self.sql)
        values = self.cursor.fetchall()
        return values

    def showcomment(self):
        self.sql = "select * from comment order by `commenttimestamp` desc"
        print(self.sql)
        self.cursor.execute(self.sql)
        values = self.cursor.fetchall()
        return values
