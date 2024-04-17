import pymysql
from flask import *

# DB 연결
def db_connect() :
    db = pymysql.connect(
        user = 'root',
        password = 'admin12345',
        host = 'coupangdb.cwshg6arkkpy.ap-northeast-1.rds.amazonaws.com',
        db = 'project',
        charset = 'utf8',
        autocommit = True
    )

    return db

# 로그인
def selectMemberById(userId) :

    result = []
    con = db_connect()

    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
    sql_select = 'SELECT * FROM admin WHERE admin_id = %s'
    cursor.execute(sql_select, userId)
    result = cursor.fetchone()

    cursor.close()
    con.close()
        

    return result



