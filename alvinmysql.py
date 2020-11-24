import pymysql
from sqlalchemy import create_engine
# import mysql
import pandas as pd

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
        return None

def getQuerryResult2Dataframe(sql, database, password, index_colname = None, ipAddress = 'localhost', username = 'root' ):
    try:
        # my_connect = mysql.connector.connect(
        #     host=ipAddress,
        #     user=username,
        #     passwd = password,
        #     database=database)       
        # df = pd.read_sql(sql,my_connect, index_col=index_colname, parse_dates=[index_colname])
        # return df

        engine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(username,password, ipAddress,database))
        df = pd.read_sql_query(sql, engine)
        return df 

    except:
        print ("Error: unable to fetch data using(usename: %s, database: %s)" %(username, database))
        return None


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
        n_affected = cursor.rowcount
        # print("\t updated once with sql = %s"%(sql))
    except Exception as e:
        print(e)
        print("\t Error: unable to update data using(usename: %s, database: %s)" %(username, database))
        print("SQL = " + sql)
        n_affected = None
        # 发生错误时回滚
        db.rollback()        
    finally:
        db.close()
        return n_affected

def addColMysql(database, password, tableName, ColumnName, ipAddress = 'localhost', username = 'root'):
    # open database connection
    db = pymysql.connect(ipAddress,username,password,database)
    
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:

        # first to test whether this column already exists in the table
        sql_testColumExist = "show COLUMNS from skill_dict like \"%s\"; " %(ColumnName)

        # 执行SQL语句
        row_count = cursor.execute(sql_testColumExist)
        # 获取所有记录列表
        if (row_count >0):
            print("Column %s already exsits in Table %s, adding failed!" %(ColumnName, tableName))
        else:
            sql_add = "alter table %s add column %s FLOAT;" % (tableName, ColumnName)
            # 执行SQL语句
            cursor.execute(sql_add)
            # 提交到数据库执行
            db.commit()
            print("\t successfully added Column %s into Table %s." %(ColumnName, tableName))
    except Exception as e:
        print(e)
        print("\t Error: unable to update data using(usename: %s, database: %s)" %(username, database))
        print("SQL = " + sql_add)
        # 发生错误时回滚
        db.rollback()        
    finally:
        db.close()
        return


def getMysqlConnection(sql, database, password, ipAddress = 'localhost', username = 'root' ):
    # Get the connection of mysql
    db = pymysql.connect(ipAddress,username,password,database)

    return db