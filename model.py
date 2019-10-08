import pymysql
import json
import datetime



conf = json.load(open("server_conf.json",encoding = "utf-8"))  # 加载配置信息


def increase_mearch(a,b,c,d,e):
    '''
    函数功能：增加商品
    参数：（商品名称，商品分类，商品价格，商品规格，照片名称）
    返回值：增加成功返回0，增加失败返回1,商品已存在返回2
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    try:
        with conn.cursor() as cur:
            # print("insert into merchinfo  values (default,%s,%s,%s,%s,default,%s)"%(a,b,c,d,e))
            cur.execute("select MerchName from merchinfo where MerchName=%s", (a))
            if cur.rowcount == 0:
                cur.execute('insert into merchinfo  values (default,%s,%s,%s,%s,default,%s)', (a,b,c,d,e))
                conn.commit()
                return 0
            else:
                return 2
    except:
        return 1

    finally:
        cur.close()

def delete_mearch(a):
    '''
    函数功能：删除商品
    参数：（商品名称）
    返回值：删除成功返回0，删除失败返回1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    try:
        with conn.cursor() as cur:
                cur.execute('UPDATE merchinfo SET MerchState = %s WHERE MerchName = %s',(2,a))
                conn.commit()
                return 0
    except:
        return 1
    finally:
        cur.close()


def change_mearch(a,b,c):
    '''
    函数功能：修改商品信息
    参数：（修改商品名，修改商品价格，商品ID）
    返回值：修改成功返回0，修改失败返回1,要修改的商品已经存在返回2
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    if len(a.strip())==0 or len(b.strip())==0 or len(c.strip())==0:
        return 1

    try:
        with conn.cursor() as cur:
            cur.execute("select MerchName from merchinfo where MerchID=%s", (c))
            old_MerchName = cur.fetchone()
            if old_MerchName:
                old_MerchName = old_MerchName[0]
                print(old_MerchName)
            if old_MerchName != a:
                cur.execute("select MerchName from merchinfo where MerchName=%s", (a))
                if cur.rowcount == 0:
                    cur.execute('UPDATE merchinfo SET MerchName = %s , MerchPrice = %s WHERE  MerchID = %s',(a,b,c))
                    conn.commit()
                    return 0
                else:
                    return 2
            else:
                cur.execute('UPDATE merchinfo SET MerchName = %s , MerchPrice = %s WHERE  MerchID = %s',(a,b,c))
                conn.commit()
                return 0
                
    except:
        return 1
    finally:
        cur.close()

def find_mearch_name(a,page,pagesize):
    '''
    函数功能：根据商品名查找商品
    参数：（商品名称,页码,每页显示数量）
    返回值：查找成功返回商品信息（元组数据类型），查找失败返回1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    page = (page-1)*pagesize
    try:
        with conn.cursor() as cur:
            cur.execute("select * from merchinfo where MerchName Like '%{0}%' limit {1},{2}".format(a,page,pagesize))
            row = cur.fetchall()
            return row          
    except:
        return 1
    finally:
        cur.close()

def find_mearch_count(a):
    '''
    函数功能：根据商品名查找商品数量
    参数：（商品名称）
    返回值：查找成功返回商品数量，查找失败返回-1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

   
    try:
        with conn.cursor() as cur:
            cur.execute("select * from merchinfo where MerchName Like '%{0}%'".format(a))
            info_num = cur.rowcount
            return info_num          
    except:
        return -1
    finally:
        cur.close()




def find_mearch_type(a):
    '''
    函数功能：根据商品类型查找商品
    参数：（商品类型）
    返回值：查找成功返回商品信息（元组数据类型），查找失败返回1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    try:
        with conn.cursor() as cur:
            cur.execute('select * from merchinfo where MerchType = %s',(a))
            row = cur.fetchall()
            return row
    except:
        return 1
    finally:
        cur.close()


def find_mearch_photo(a):
    '''
    函数功能：根据商品照片名查找商品
    参数：（商品照片名）
    返回值：查找成功返回商品信息（元组数据类型），查找失败返回1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    try:
        with conn.cursor() as cur:
            cur.execute('select * from merchinfo where MerchPhoto = %s',(a))
            row = cur.fetchall()
            return row
    except:
        return 1
    finally:
        cur.close()



def order_add(uid):
    '''
    函数功能：增加订单，
    函数参数：uid 订单的用户ID
    函数返回值：增加成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("insert into ordertable values(default,%s,default)"%uid)
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def order_update(OrderID):
    '''
    函数功能：修改订单状态，
    函数参数：OrderID 订单ID
    函数返回值：修改成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("update ordertable set OrderState=2 where OrderID=%s"%OrderID)
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def order_inquire(key,value):
    '''
    函数功能：查找订单，
    函数参数：key 查找的键,value查找的值
    函数返回值：修改成功返回查找数据，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    sql = "select * from ordertable where {0} ='{1}'".format(key,value)
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute(sql)
            rows = cur.fetchall()  
            return rows    #返回查找结果集
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 



def orderinfo_add(OrderID,MerchID,MerchName,Num,price):
    '''
    函数功能：增加订单信息，
    函数参数：OrderID，MerchID，MerchName，Num，price
    函数返回值：增加成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("insert into orderinfo values(%s,%s,%s,%s,%s)",(OrderID,MerchID,MerchName,Num,price))
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 



