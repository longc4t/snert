from config import app
from config import sqlite3


def init_db():
    conn = sqlite3.connect('./user.db')
    cursor = conn.cursor()
    sql = '''   create table user(
                userid int auto_increment primary key,
                username varchar(50),
                password varchar(50),
                token varchar(100),
                personsay varchar(200),
                userarticle int,
                usercomment int
                );
          '''
    cursor.execute(sql)
    
    sql= '''    create table article(
                articleid int auto_increment primary key,
                articletitle varchar(50),
                articleauthor varchar(50),
                articleauthorid int,
                articlecontent varchar(500),
                articletimestamp varbinary(8),
                commentid int
                );
        '''
    cursor.execute(sql)
    sql = '''   create table comment(
                commentid int auto_increment primary key,
                commentauthor varchar(50),
                commentauthorid int,
                commentcontent varchar(500),
                commenttimestamp varbinary(8)
                );
          '''
    cursor.execute(sql)
    cursor.close()



if __name__ == '__main__':
    init_db()
    app.run()

