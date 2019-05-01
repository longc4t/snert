import sqlite3


class sqlop:
    def __init__(self):
        self.conn=sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.sql=""

    def select(self,field=(),tablename="",selectkey="",selectvalue=""):
        self.sql = "select {field} from {tablename} WHERE {selectkey}= '{selectvalue}'".format(field=field,
                                                                                             tablename=tablename,
                                                                                             selectkey=selectkey,
                                                                                             selectvalue=selectvalue)
        print(self.sql)
        self.cursor.execute(self.sql)
        values = self.cursor.fetchall()
        return values

    def update(self,field=(),tablename="",newvalue="",updatekey="",updatevalue=""):
        self.sql="update {tablename} set {field}={newvalue} where {updatekey}='{updatevalue}'".format(tablename=tablename,
                                                                                                    field=field,
                                                                                                    newvalue=newvalue,
                                                                                                    updatekey=updatekey,
                                                                                                    updatevalue=updatevalue)
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()

    def insert(self,tablename="",insertvalue=()):

        self.sql="INSERT INTO {tablename} VALUES {insertvalue}".format(tablename=tablename,insertvalue=insertvalue)
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()


