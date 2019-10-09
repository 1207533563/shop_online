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

def inquire_Merch_ByID(a):
    '''
    函数功能：根据商品ID查找商品信息
    参数：（商品ID）
    返回值：查找成功返回商品信息，查找失败返回1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:
            cur.execute("select * from merchinfo where MerchID=%s",(a))
            row = cur.fetchall()
            return row         
    except:
        return -1
    finally:
        cur.close()

def find_type_count(a):
    '''
    函数功能：根据商品大类查找商品数量
    参数：（商品大类）
    返回值：查找成功返回商品数量，查找失败返回-1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    if a =="零食":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "早餐面包" or MerchType= "膨化食品" or MerchType="方便速食" or MerchType="其他零食" '
    elif a =="酒水饮料":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "啤酒" or MerchType= "碳酸饮料" or MerchType="其他酒水饮料" '
    elif a =="生活用品":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "洗浴用品" or MerchType= "其他生活用品" or MerchType="其他生活用品" '
    elif a =="":
        sql = 'select * from merchinfo '
    else:
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "杂货"'
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
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



def find_Type(a,page,pagesize):
    '''
    函数功能：根据商品大类查找商品
    参数：（商品类型,页码,每页显示数量）
    返回值：查找成功返回商品信息（元组数据类型），查找失败返回1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    page = (page-1)*pagesize

    if a =="零食":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "早餐面包" or MerchType= "膨化食品" or MerchType="方便速食" or MerchType="其他零食" limit {0},{1}'.format(page,pagesize)
    elif a =="酒水饮料":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "啤酒" or MerchType= "碳酸饮料" or MerchType="其他酒水饮料" limit {0},{1}'.format(page,pagesize)
    elif a =="生活用品":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "洗浴用品" or MerchType= "其他生活用品" or MerchType="其他生活用品" limit {0},{1}'.format(page,pagesize)
    elif a =="":
        sql = 'select * from merchinfo  limit {0},{1}'.format(page,pagesize)
    else:
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "杂货" limit {0},{1}'.format(page,pagesize)
        
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
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



def orderaddr_add(uname, Receiver, ShipPhone, Adress):
    '''
    函数功能：增加地址，
    函数参数：uname 用户名
    函数返回值：增加成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("insert into shipaddr values(default,%s,%s,%s,%s,default)",(uname, Receiver, ShipPhone, Adress))
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def orderaddr_del(uid):
    '''
    函数功能：删除地址，
    函数参数：uid 用户ID
    函数返回值：增加成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("update shipaddr set AddrState=%s where addrID=%s",(2,uid))
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 



def orderaddr_update(Receiver, ShipPhone, Adress,addrID):
    '''
    函数功能：修改地址，
    函数参数：uid 订单的用户ID
    函数返回值：修改成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("update shipaddr set Receiver=%s, ShipPhone=%s, Adress=%s where addrID=%s",(Receiver, ShipPhone, Adress, addrID))
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def orderaddr_inquire_name(uname):
    '''
    函数功能：查看地址，
    函数参数：uname,查找的用户名
    函数返回值：修改成功返回查找数据，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute( "select addrID,Receiver,ShipPhone,Adress from shipaddr where uname=%s and AddrState=%s ",(uname,1))
            rows = cur.fetchall()  
            return rows    #返回查找结果集
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def orderaddr_inquire_ID(addrID):
    '''
    函数功能：查看地址，
    函数参数：addrID,查找的地址编号
    函数返回值：修改成功返回查找数据，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute( "select Receiver,ShipPhone,Adress from shipaddr where addrID=%s and AddrState=%s ",(addrID,1))
            rows = cur.fetchall()  
            return rows    #返回查找结果集
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


