import pymysql
import json
import datetime



conf = json.load(open("server_conf.json",encoding = "utf-8"))  # 加载配置信息


def order_add(uid, uname, Receiver, ShipPhone, Adress):
    '''
    函数功能：增加地址，
    函数参数：uid 订单的用户ID
    函数返回值：增加成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("insert into shipaddr values(%s,%s,%s,%s,%s)"%(uid, uname, Receiver, ShipPhone, Adress))
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def order_del(uid):
    '''
    函数功能：删除地址，
    函数参数：uid 订单的用户ID
    函数返回值：增加成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("delete from shipaddr where uid=%s"%uid)
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def order_update(uid, uname, Receiver, ShipPhone, Adress):
    '''
    函数功能：修改地址，
    函数参数：uid 订单的用户ID
    函数返回值：修改成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("update shipaddr set uid=%s, uname=%s, Receiver=%s, ShipPhone=%s, Adress=%s where uid=%s"%(uid, uname, Receiver, ShipPhone, Adress, uid))
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def order_inquire(uid, key, value):
    '''
    函数功能：查看地址，
    函数参数：key 查找的键,　value查找的值
    函数返回值：修改成功返回查找数据，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    sql = ("select * from shipaddr where uid=%s"%uid).format(key,value)
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute(sql)
            rows = cur.fetchall()  
            return rows    #返回查找结果集
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 



