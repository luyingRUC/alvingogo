import pymysql

def getQuerryResult(sql, database, password, ipAddress = 'localhost', username = 'root' ):
    # open database connection
    db = pymysql.connect(ipAddress,username,password,database)
    
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:
        # 执行SQL语句
        row_count = cursor.execute(sql)
        # 获取所有记录列表
        if (row_count >0):
            results = cursor.fetchall()
            return results
        else:
            return None
        db.close()

    except:
        print ("Error: unable to fetch data using(usename: %s, database: %s)" %(username, database))
        db.close()
        return 


def updateMysql(sql, database, password, ipAddress = 'localhost', username = 'root'):
    # open database connection
    db = pymysql.connect(ipAddress,username,password,database)
    
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("\t successfully updated once")
    except Exception as e:
        print(e)
        print ("\t Error: unable to update data using(usename: %s, database: %s)" %(username, database))
        # 发生错误时回滚
        db.rollback()        
    finally:
        db.close()
        return