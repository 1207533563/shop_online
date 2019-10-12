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
            cur.execute("select MerchName,MerchState from merchinfo where MerchName=%s", (a))
            if cur.rowcount == 0:
                cur.execute('insert into merchinfo  values (default,%s,%s,%s,%s,default,%s)', (a,b,c,d,e))
                conn.commit()
                return 0
            elif cur.rowcount > 0:
                rows = cur.fetchone()
                
                if rows[1] == '2':
                    cur.execute('update merchinfo set MerchState=1,MerchPhoto=%s where MerchName=%s', (e,a))
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
    参数：（商品ID）
    返回值：删除成功返回0，删除失败返回1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    print(a)
    try:
        with conn.cursor() as cur:
                cur.execute('UPDATE merchinfo SET MerchState = 2 WHERE MerchID = %s',(a))
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
            cur.execute("select * from merchinfo where MerchName Like '%{0}%' AND MerchState=1 limit {1},{2}".format(a,page,pagesize))
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
            cur.execute("select * from merchinfo where MerchName Like '%{0}%' AND MerchState=1".format(a))
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
            cur.execute("select * from merchinfo where MerchID=%s AND MerchState=1",(a))
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
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "早餐面包" or MerchType= "膨化食品" or MerchType="方便速食" or MerchType="其他零食" AND MerchState=1'
    elif a =="酒水饮料":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "啤酒" or MerchType= "碳酸饮料" or MerchType="其他酒水饮料" AND MerchState=1'
    elif a =="生活用品":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "洗浴用品" or MerchType= "其他生活用品" or MerchType="其他生活用品" AND MerchState=1'
    elif a =="":
        sql = 'select * from merchinfo where MerchState=1'
    else:
        sql =  'SELECT * FROM merchinfo WHERE MerchType ="杂货" AND MerchState=1'
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
            cur.execute('select * from merchinfo where MerchType = %s AND MerchState=1',(a))
            row = cur.fetchall()
            return row
    except:
        return 1
    finally:
        cur.close()



def find_Type(a,page,pagesize):
    '''
    函数功能：根据商品大类查找商品信息
    参数：（商品类型,页码,每页显示数量）
    返回值：查找成功返回商品信息（元组数据类型），查找失败返回1
    '''
    conn=pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"],
                                   passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    page = (page-1)*pagesize

    if a =="零食":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "早餐面包" or MerchType= "膨化食品" or MerchType="方便速食" or MerchType="其他零食" AND MerchState=1 limit {0},{1}'.format(page,pagesize)
    elif a =="酒水饮料":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "啤酒" or MerchType= "碳酸饮料" or MerchType="其他酒水饮料" AND MerchState=1 limit {0},{1}'.format(page,pagesize)
    elif a =="生活用品":
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "洗浴用品" or MerchType= "其他生活用品" or MerchType="其他生活用品" AND MerchState=1 limit {0},{1}'.format(page,pagesize)
    elif a =="":
        sql = 'select * from merchinfo where MerchState=1 limit {0},{1}'.format(page,pagesize)
    else:
        sql =  'SELECT * FROM merchinfo WHERE MerchType = "杂货" AND MerchState=1 limit {0},{1}'.format(page,pagesize)
    
    
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


def order_add(addrID,Merchsum,Info):
    '''
    函数功能：增加订单，
    函数参数：uid 订单的用户ID
    函数返回值：增加成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("insert into ordertable values(default,%s,default,sysdate(),%s)",(addrID,Merchsum))
            conn.commit()
            cur.execute("select max(OrderID) from ordertable where addrID=%s"%addrID)
            row=cur.fetchone()[0]
            
            for i in eval(Info):            
                MerchID = i[0]
                MerchName =i[1]
                Num = i[2]
                price = i[3]
                MerchPhoto = i[4]
                cur.execute("insert into orderinfo (OrderID,MerchID,MerchName,Num,price,MerchPhoto) values(%s,%s,%s,%s,%s,%s)",(row,MerchID,MerchName,Num,price,MerchPhoto))
                conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def order_remove(OrderID):
    '''
    函数功能：删除订单，
    函数参数：OrderID 订单ID
    函数返回值：删除成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("update ordertable set OrderState=3 where OrderID=%s"%OrderID)
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 





def order_update(OrderID):
    '''
    函数功能：订单确认收货，
    函数参数：OrderID 订单ID
    函数返回值：成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("update ordertable set OrderState=2 where OrderID=%s"%(OrderID))
            conn.commit()  
            # cur.execute("update orderinfo set MerchID=%s,MerchName=%s,Num=%s,price=%s,Merchsum=%s where OrderID=%s",(MerchID,MerchName,Num,price,Merchsum,OrderID))
            # conn.commit() 
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def order_inquire(uname):
    '''
    函数功能：查找订单，
    函数参数：OrderID 订单编号
    函数返回值：查找成功返回查找数据，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

    # print(("SELECT OrderID FROM ordertable WHERE addrID in (SELECT addrID FROM shipaddr WHERE uname=%s)"%uname))
 
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("SELECT * FROM ordertable WHERE OrderState<>3 and addrID in (SELECT addrID FROM shipaddr WHERE uname='%s' and Addrstate=1)"%uname)
            rows_1 = cur.fetchall()  
            # print(rows_1)
            list_1=[]
            
            for i in rows_1:
                temp = list(i)
                temp.append([])
                list_1.append(temp)
            
 
            cur.execute("SELECT * FROM orderinfo WHERE OrderID in(SELECT OrderID FROM ordertable WHERE OrderState<>3 and addrID in (SELECT addrID FROM shipaddr WHERE uname='%s' and Addrstate=1))"%uname)
            rows_2 = cur.fetchall() 
           
            list_2=list(rows_2)
       
            for i in list_1:
                for j in list_2:
                    if j[0]==i[0]:
                        
                        i[5].append(j)

            
            list_1_1=[]
            for i in list_1:
                list_1_1.append(tuple(i))
            rows_1_1=tuple(list_1_1)

            
            
            return rows_1_1  #返回查找结果集
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


###########################################购物车增删改查#######################################
def shoppingcart_add(uname,MerchID,MerchName,Num,price,MerchPhoto):
    '''
    函数功能：将商品增加到购物车，
    函数参数：uname  用户名,MerchID 商品ID,MerchName 商品名,Num 商品数量,price,MerchPhoto
    函数返回值：增加成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:

        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("select Num from shoppingcart where uname=%s and MerchID=%s ",(uname,MerchID))
            if cur.rowcount == 0:
                cur.execute("insert into shoppingcart (uname,MerchID,MerchName,Num,price,MerchPhoto) values(%s,%s,%s,%s,%s,%s)",(uname,MerchID,MerchName,Num,price,MerchPhoto))
                conn.commit()  
                return 0   
            else :
                new_num = int(cur.fetchone()[0]) + int(Num)
                cur.execute("update shoppingcart set Num=%s where MerchID=%s and uname=%s",(new_num,MerchID,uname))
                conn.commit()
                return 0
           
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def shoppingcart_one_remove(uname,MerchID):
    '''
    函数功能：删除指定用户名的某件商品，
    函数参数：uname 用户名,MerchID 商品ID（通过用户名和商品ID删除单个商品）
    函数返回值：删除成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("DELETE FROM shoppingcart WHERE uname=%s and MerchID=%s",(uname,MerchID))
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 

def shoppingcart_all_remove(uname):
    '''
    函数功能：清空购物车，
    函数参数：uname 用户名 (通过用户名删除购物车所有商品)
    函数返回值：删除成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("DELETE FROM shoppingcart WHERE uname='%s'"%uname)
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 




def shoppingcart_update(uname,MerchID,Num):
    '''
    函数功能：修改购物车某件商品数量，
    函数参数：uname 用户名,MerchID  商品ID,Num 商品数量（通过用户名和商品ID来修改商品数量）
    函数返回值：修改成功返回0，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("update shoppingcart set Num=%s where MerchID=%s and uname=%s",(Num,MerchID,uname))
            conn.commit()  
            return 0   
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 


def shoppingcart_inquire(uname):
    '''
    函数功能：查找某用户的所有购物车商品，
    函数参数：uname 用户名（通过用户名查找该用户购物车所有商品）
    函数返回值：查找成功返回查找数据，失败返回1
    '''
    conn = pymysql.connect(host=conf["db_server_ip"], port=conf["db_server_port"], user=conf["db_user"], passwd=conf["db_password"], db=conf["db_name"], charset="utf8")

 
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            cur.execute("SELECT * FROM shoppingcart WHERE uname='%s'"%uname)
            rows_1 = cur.fetchall()  
            return rows_1  #返回查找结果集
    finally: 
        # 关闭数据库连接
        conn.close()         
    return 1 