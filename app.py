import os, re, random, json, urllib.parse, urllib.request,datetime,math
from flask import Flask, render_template, request, jsonify, session,abort,redirect,url_for,Response
import pymysql
import model

conf = json.load(open("server_conf.json"))  # 加载配置信息



app = Flask(__name__)
app.secret_key = b'N\x1cI\xcf6\xe1\x98\xa1\x06\x0c\x8f\x05\xf7\xca\xe6\xa0H0\xa7B\xfc\xde\xd7i'

app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static\products") 

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login_handle():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        upass = request.form.get("upass")
        
        if not (uname and uname.strip() and upass and upass.strip()):
            abort(Response("登录失败"))
 
        if not re.fullmatch("[a-zA-Z0-9_]{4,20}",uname):
            abort(Response("用户名不合法!"))

        if not(len(upass) >= 6 and len(upass) <= 16):
            abort(Response("密码格式错误！"))

        conn =pymysql.connect(
            host=conf["db_server_ip"],
            port=conf["db_server_port"],
            user=conf["db_user"],
            passwd=conf["db_password"],
            db=conf["db_name"],
            charset ='utf8'
        )
    
        with conn.cursor() as cur:
            cur.execute("SELECT * from shop_user where uname=%s and upass=md5(%s)", (uname,uname+upass))
            res = cur.fetchone()
            
        if res:
            #登录成功跳转首页
            cur_login_time = datetime.datetime.now()
            user_info = {
                "uid":res[0],
                "uname":res[1],
                "upass":res[2],
                "phone":res[3],
                
                "reg_time":res[4],
                "last_login_time":res[5],
                "priv":res[6],
                "state":res[7],
                "login_time": cur_login_time
            }          
            session["user_info"] = user_info

            try:
                with conn.cursor() as cur:
                    cur.execute("update shop_user set last_login_time=%s where uid=%s ",(cur_login_time,res[0]))
                    conn.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(e)
            finally:
                conn.close()
        
        else:
            #登录失败

            return render_template("login.html",login_fail=1)



@app.route("/reg", methods=["GET", "POST"])
def reg_handle():
    if request.method == "GET":
        return render_template("reg.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        upass = request.form.get("upass")
        upass2 = request.form.get("upass2")
        phone = request.form.get("phone")
        verify_code = request.form.get("verify_code")
        

        if not (uname and uname.strip() and upass and upass2 and phone and verify_code):
            abort(500)
 
        if not re.fullmatch("[a-zA-Z0-9_]{4,20}",uname):
            abort(Response("用户名不合法!"))
        
        conn =pymysql.connect(
            host=conf["db_server_ip"],
            port=conf["db_server_port"],
            user=conf["db_user"],
            passwd=conf["db_password"],
            db=conf["db_name"],
            charset ='utf8'
        )

        with conn.cursor() as cur:
            cur.execute("SELECT uid from shop_user where uname=%s", (uname,))
            if cur.rowcount != 0:
                abort(Response("用户名已经被注册!"))

        if not(len(upass) >= 6 and len(upass) <= 16 and upass == upass2):
            abort(Response("密码格式错误！"))
 
        if  session.get(phone) != verify_code:
            abort(Response("验证码错误!"))

      

        try:
            with conn.cursor() as cur:
                cur.execute("insert into shop_user values(DEFAULT, %s, md5(%s), %s, sysdate(), sysdate(), 1, 1)",(uname,uname + upass,phone))
                conn.commit()
        except:
            abort(Response("注册失败！"))  
        finally:
            conn.close()

        session.pop(phone)  
        return redirect(url_for("login_handle"))


@app.route("/logout")  #注销
def logout_handle():
    res = {"err": 1,"desc":"未登录！"}
    if session.get("user_info"):
        session.pop("user_info")
        res["err"] = 0
        res["desc"] = "注销成功！"
    return jsonify(res)


#找回密码
@app.route("/repasswd", methods=["GET", "POST"])
def repasswd():
    if request.method == "GET":
        return render_template("repasswd.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        phone = request.form.get("phone")
        verify_code = request.form.get("verify_code")
        upass = request.form.get("upass")
        upass2 = request.form.get("upass2")

        conn =pymysql.connect(
            host=conf["db_server_ip"],
            port=conf["db_server_port"],
            user=conf["db_user"],
            passwd=conf["db_password"],
            db=conf["db_name"],
            charset ='utf8'
        )

        with conn.cursor() as cur:
            cur.execute("SELECT uid from shop_user where uname=%s and phone=%s", (uname,phone))
            if cur.rowcount == 0:
                abort(Response("绑定手机号不正确!"))

        if not(len(upass) >= 6 and len(upass) <= 16 and upass == upass2):
            abort(Response("密码格式错误！"))
 
        if  session.get(phone) != verify_code:
            abort(Response("验证码错误!"))

        try:
            with conn.cursor() as cur:
                cur.execute("update shop_user set upass=md5(%s) where uname=%s and phone=%s", (uname+upass,uname,phone))
                conn.commit()
        finally:
            session.pop(phone)
            conn.close()
        return redirect(url_for("login_handle"))


@app.route("/product_manage")  #商品管理
def merch_manage():
    return render_template("product_manage.html")


@app.route("/product_list")  #商品列表
def product_list():
    return render_template("product_list.html")

@app.route("/receiver_address")  #收货地址
def receiver_address():
    return render_template("receiver_address.html")

@app.route("/orderaddr_update")  #修改收货地址
def orderaddr_update():
    addrID = request.args.get("addrID")
    return render_template("orderaddr_update.html",addrID=addrID)


@app.route("/update_product")  #修改商品
def update_product():
    MerchID = request.args.get("MerchID")
    print(MerchID)
    return render_template("update_product.html",MerchID=MerchID)

@app.route("/user_orders")  #订单
def user_orders():
    return render_template("user_orders.html")

@app.route("/shop_cart")  #订单
def shop_cart():
    return render_template("shop_cart.html")
    


@app.route("/add_merch", methods=["GET", "POST"])  #添加商品
def add_merch():
    if request.method == "GET":
        return render_template("add_merch.html")
    elif request.method == "POST":
        MerchName = request.form.get("MerchName")
        MerchType = request.form.get("MerchType")
        MerchPrice = request.form.get("MerchPrice")
        MerchUnit = request.form.get("MerchUnit")
        MerchPhoto = request.files["MerchPhoto"]
        MerchPhoto_name = MerchPhoto.filename
        print(MerchPhoto_name)
        print(MerchType)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], MerchPhoto_name)
        MerchPhoto.save(file_path)


        res = {"err": 1,"desc":"内部错误！"
            }  
        rsp = model.increase_mearch(MerchName,MerchType,MerchPrice,MerchUnit,MerchPhoto_name)
        if rsp == 0:
            res["err"] = 0
            res["desc"] = "增加成功！"
        elif rsp == 2:
            res["err"] = 2
            res["desc"] = "商品已存在"
        
        
        return res["desc"]

            

@app.route("/req_merchInfo")  #请求商品信息接口通过类型
def req_merchInfo():
    MerchType = request.args.get("merchtype")
    res = {"err": 1,"MerchType":MerchType,
            "MerchInfo":{       
            }
        }  
    conn =pymysql.connect(
            host=conf["db_server_ip"],
            port=conf["db_server_port"],
            user=conf["db_user"],
            passwd=conf["db_password"],
            db=conf["db_name"],
            charset ='utf8'
        )
    try:
        with conn.cursor() as cur:
                cur.execute("select MerchName,MerchPhoto,MerchPrice from merchinfo where MerchType=%s and Merchstate=1",(MerchType))
                if cur.rowcount != 0:
                    res["err"]= 0
                    rows = cur.fetchall() 
                    
                    res["MerchInfo"]=rows
    finally:
        conn.close()
    return jsonify(res)





@app.route("/update_merch")  #修改商品信息接口
def update_merch():
    MerchName = request.args.get("MerchName")
    MerchPrice = request.args.get("MerchPrice")
    MerchID = request.args.get("MerchID")

    res = {"err": 1,"desc":"内部错误！"
        }  
    rsp = model.change_mearch(MerchName,MerchPrice,MerchID)

    if rsp == 0:
        res["err"] = 0
        res["desc"] = "修改成功！"
    elif rsp == 2:
        res["err"] = 2
        res["desc"] = "该商品已存在"
    
    return jsonify(res)


@app.route("/show_merch")  #修改商品信息网页展示商品信息的接口,按名字查找
def show_merch():
    MerchName = request.args.get("MerchName")
    page = request.args.get("page")
    pagesize = request.args.get("pagesize")
    res = {"err": 1,"desc":"内部错误！","info_num":0,"MerchInfo":{}
        }  
    rsp = model.find_mearch_name(MerchName,int(page),int(pagesize))
    
    if rsp != 1:
        res["err"] = 0
        res["desc"] = "查找成功！"
        res["MerchInfo"] = rsp  
    rsp_num = model.find_mearch_count(MerchName)
    if rsp_num != -1:
        res["info_num"] = rsp_num
    return jsonify(res)

@app.route("/inquire_Merch_ByID")  #展示商品信息的接口,按ID查找
def inquire_Merch_ByID():
    MerchID = request.args.get("MerchID")
    res = {"err": 1,"desc":"内部错误！","MerchInfo":{}
        }  
    rsp = model.inquire_Merch_ByID(MerchID)

    if rsp != 1:
        res["err"] = 0
        res["desc"] = "查找成功！"
        res["MerchInfo"] = rsp  
    return jsonify(res)


@app.route("/show_type_merch")  #展示商品信息的接口,按大类查找
def show_type_merch():
    MerchType = request.args.get("MerchType")
    page = request.args.get("page")
    pagesize = request.args.get("pagesize")
    res = {"err": 1,"desc":"内部错误！","info_num":0,"MerchInfo":{}
        }  
    rsp = model.find_Type(MerchType,int(page),int(pagesize))
    
    if rsp != 1:
        res["err"] = 0
        res["desc"] = "查找成功！"
        res["MerchInfo"] = rsp  
    rsp_num = model.find_type_count(MerchType)
    if rsp_num != -1:
        res["info_num"] = rsp_num

    print(res)
    return jsonify(res)


@app.route('/remove_merch')
def remove_merch():
    MerchID = request.args.get("MerchID")
    print(MerchID)

    res = {"err": 1,"desc":"内部错误！"
        }  
    rsp = model.delete_mearch(MerchID)
    if rsp == 0:
        res["err"] = 0
        res["desc"] = "删除成功！"

    return jsonify(res)


# @app.route("/show_orderinfo")  #查找订单
# def show_orderinfo():
#     uid = request.args.get("uid")
#     page = request.args.get("page")
#     pagesize = request.args.get("pagesize")
#     res = {"err": 1,"desc":"内部错误！","info_num":0,"MerchInfo":{}
#         } 
#     rsp = model.find_Type(MerchType,int(page),int(pagesize)) 



@app.route('/add_address')
def add_address():
    uname = request.args.get("uname")
    Receiver = request.args.get("Receiver")
    ShipPhone = request.args.get("ShipPhone")
    Adress = request.args.get("Adress")

    res = {"err": 1,"desc":"内部错误！"
        }  
    print(uname,Receiver,ShipPhone,Adress)
    rsp = model.orderaddr_add(uname,Receiver,ShipPhone,Adress)
    if rsp == 0:
        res["err"] = 0
        res["desc"] = "增加成功！"

    return jsonify(res)


@app.route('/remove_address')
def remove_address():
    addrID = request.args.get("addrID")

    res = {"err": 1,"desc":"内部错误！"
        }  
    rsp = model.orderaddr_del(addrID)
    if rsp == 0:
        res["err"] = 0
        res["desc"] = "删除成功！"

    return jsonify(res)


@app.route('/change_address')
def change_address():
    Receiver = request.args.get("Receiver")
    ShipPhone = request.args.get("ShipPhone")
    Adress = request.args.get("Adress")
    addrID = request.args.get("addrID")

    res = {"err": 1,"desc":"内部错误！"
        }  
    rsp = model.orderaddr_update(Receiver,ShipPhone,Adress,addrID)
    if rsp == 0:
        res["err"] = 0
        res["desc"] = "修改成功！"

    return jsonify(res)


@app.route('/find_name_address')
def find_name_address():
    uname = request.args.get("uname")
    res = {"err": 1,"desc":"内部错误！","addrinfo":{}
        }  
    rsp = model.orderaddr_inquire_name(uname)
    if rsp != 1:
       res["err"]= 0
       res["desc"]= "查找成功"
       res["addrinfo"]= rsp

    return jsonify(res)


@app.route('/find_ID_address')
def find_ID_address():
    addrID = request.args.get("addrID")
    res = {"err": 1,"desc":"内部错误！","addrinfo":{}
        }  
    rsp = model.orderaddr_inquire_ID(addrID)
    print(rsp)
    if rsp != 1:
       res["err"]= 0
       res["desc"]= "查找成功"
       res["addrinfo"]= rsp

    return jsonify(res)


##############################订单增删改查############################
@app.route('/order_add')
def order_add():
    addrID = request.args.get('addrID')
    Merchsum = request.args.get('orderPrice')
    Info = request.args.get('orderInfo')
    
    rsp=model.order_add(addrID,Merchsum,Info)
    res={
        "err":1,"desc":"内部错误"
    }
    if rsp == 0:
        res["err"]=0
        res["desc"] = "订单添加成功"
    return jsonify(res)


@app.route('/order_remove')
def order_remove():
    OrderID = request.args.get('OrderID')
    
    res={
        "err":1,"desc":"内部错误"
    }
    rsp=model.order_remove(OrderID)
    if rsp == 0:
        res["err"]=0
        res["desc"] = "订单删除成功"
    return jsonify(res)



@app.route('/order_change')
def order_change():
    OrderID = request.args.get('OrderID')
    res={
        "err":1,"desc":"内部错误"
    }
    rsp=model.order_update(OrderID)
    if rsp == 0:
        res["err"]=0
        res["desc"] = "订单收货成功"
    return jsonify(res)



@app.route('/order_find')
def order_find():
    uname = request.args.get('uname')
    res={
        "err":1,"desc":"内部错误","OrderInfo":{}
    }
    rsp=model.order_inquire(uname)
    if rsp != 1:
        res["err"]=0
        res["desc"] = "订单查询成功"
        res["OrderInfo"] =rsp
    return jsonify(res)



##############################购物车的增删改查############################
@app.route('/shoppingcart_add')
def shoppingcart_add():
    MerchID = request.args.get('MerchID')
    MerchName = request.args.get('MerchName')
    Num = request.args.get('Num')
    price = request.args.get('price')
    uname = request.args.get('uname')
    MerchPhoto = request.args.get("MerchPhoto")
    res={
        "err":1,"desc":"内部错误"
    }
    rsp=model.shoppingcart_add(uname,MerchID,MerchName,Num,price,MerchPhoto)
    if rsp == 0:
        res["err"]=0
        res["desc"] = "商品添加购物车成功"
    return jsonify(res)


@app.route('/shoppingcart_one_remove')
def shoppingcart_one_remove():
    uname = request.args.get('uname')
    MerchID = request.args.get('MerchID')
    res={
        "err":1,"desc":"内部错误"
    }
    rsp=model.shoppingcart_one_remove(uname,MerchID)
    if rsp == 0:
        res["err"]=0
        res["desc"] = "商品删除成功"
    return jsonify(res)

@app.route('/shoppingcart_all_remove')
def shoppingcart_all_remove():
    uname = request.args.get('uname')
    res={
        "err":1,"desc":"内部错误"
    }
    rsp=model.shoppingcart_all_remove(uname)
    if rsp == 0:
        res["err"]=0
        res["desc"] = "商品删除成功"
    return jsonify(res)


@app.route('/shoppingcart_change')
def shoppingcart_change():
    uname = request.args.get("uname")
    MerchID = request.args.get('MerchID')
    Num = request.args.get('Num')
    res={
        "err":1,"desc":"内部错误"
    }
    rsp=model.shoppingcart_update(uname,MerchID,Num)
    if rsp == 0:
        res["err"]=0
        res["desc"] = "数量修改成功"
    return jsonify(res)



@app.route('/shoppingcart_find')
def shoppingcart_find():
    uname = request.args.get('uname')
    res={
        "err":1,"desc":"内部错误","shoppingcartinfo":{}
    }
    rsp=model.shoppingcart_inquire(uname)
    if rsp !=1:
        res["err"]=0
        res["desc"] = "查询成功"
        res["shoppingcartinfo"] =rsp
    return jsonify(res)





@app.route("/send_sms_code")
def send_sms_code_handle():
    phone = request.args.get("phone")

    result = {"err": 1, "desc": "内部错误！"}
    # verify_code = send_sms_code(phone)  #发送验证码
    verify_code = "1234"
    if verify_code:
        # 发送短信验证码成功
        session[phone] = verify_code
        
        result["err"] = 0
        result["desc"] = "发送短信验证码成功！"

    return jsonify(result)

def send_sms_code(phone):
    '''
    函数功能：发送短信验证码（6位随机数字）
    函数参数：
    phone 接收短信验证码的手机号
    返回值：发送成功返回验证码，失败返回False
    '''
    verify_code = str(random.randint(100000, 999999))

    try:
        url = "http://v.juhe.cn/sms/send"
        params = {
            "mobile": phone,  # 接受短信的用户手机号码
            "tpl_id": "162901",  # 您申请的短信模板ID，根据实际情况修改
            "tpl_value": "#code#=%s" % verify_code,  # 您设置的模板变量，根据实际情况修改
            "key": "ab75e2e54bf3044898459cb209b195e4",  # 应用APPKEY(应用详细页查询)
        }
        params = urllib.parse.urlencode(params).encode()

        f = urllib.request.urlopen(url, params)
        content = f.read()
        res = json.loads(content)
        
        print(res)

        if res and res['error_code'] == 0:
            return verify_code
        else:
            return False
    except:
        return False   





if __name__ == "__main__":
    app.run(port=80, debug=True)



