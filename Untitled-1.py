import tkinter as tk
import pymssql as ssms
import random as rd
import datetime as date
def randstr(len):
    base='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    otc=''
    for i in range(len):
        otc+=base[rd.randint(0,25)]
    return otc
def randint(len):
    otc=''
    for i in range(len):
        otc+=str(rd.randint(0,9))
    return otc
class login():
    def __init__(self):
        def toggle():
            if(self.input2.cget('show')):
                self.input2.config(show='')
                self.showcode.config(text='隐藏\n密码')
            else:
                self.input2.config(show='*')
                self.showcode.config(text='显示\n密码')
        def log():
            strg=username.get();tem=strg
            if(not strg):
                self.notice.config(text='请输入账号')
                return
            if(len(strg)>8):
                cur.execute('select account from Users where email=%s',strg)
                strg=cur.fetchone()
                if(not strg):
                    self.notice.config(text='账号或密码错误')
                    return
                tem=strg=strg[0].rstrip()
            cur.execute('select password from LoginInfo where account=%s',strg)
            strg=cur.fetchone()
            if(strg and strg[0].rstrip()==code.get()):
                global account
                account=tem
                self.main.destroy()
            else:self.notice.config(text='账号或密码错误')
        def reg():
            strg,tem1,tem2=username.get(),randstr(8),code.get()
            if(not strg):
                self.notice.config(text='请输入账号')
                return
            if(not tem2):
                self.notice.config(text='请设置密码')
                return
            cur.execute('insert into Users(account,email,registerDate,creditLevel) values(%s,%s,%s)',(tem1,strg,str(date.date.today()),'5'))
            cur.execute('insert into LoginInfo(account,password) values(%s,%s)',(tem1,tem2))
            tradeinfo.commit()
            global account
            account=tem1
            self.main.destroy()
        self.main=tk.Tk()
        self.main.title('登录')
        self.main.resizable(0,0)
        self.main.geometry('400x300+450+200')
        tk.Label(self.main,font=('times',12),anchor='e',text='邮箱或账号').place(x=30,y=50,width=90,height=30)
        tk.Label(self.main,font=('times',12),anchor='e',text='密码').place(x=80,y=100,width=40,height=30)
        username,code=tk.StringVar(),tk.StringVar()
        tk.Entry(self.main,font=('times',12),textvariable=username).place(x=125,y=50,width=240,height=30)
        self.input2=tk.Entry(self.main,font=('times',12),show='*',textvariable=code)
        self.input2.place(x=125,y=100,width=240,height=30)
        self.showcode=tk.Button(self.main,text='显示\n密码',command=toggle)
        self.showcode.place(x=370,y=98,width=30,height=35)
        tk.Button(self.main,text='登录',anchor='center',command=log).place(x=100,y=180,width=80,height=40)
        tk.Button(self.main,text='注册',anchor='center',command=reg).place(x=240,y=180,width=80,height=40)
        self.notice=tk.Label(self.main,font=('times',10),anchor='w')
        self.notice.place(x=125,y=15,width=300,height=25)
class menupage():
    def __init__(self):
        def infor():
            personalinfo().main.transient()
        def collect():
            collectionpage().main.transient()
        def market():
            marketpage().main.transient()
        def sell():
            sellgoods().main.transient()
        def purch():
            purchasemanage().main.transient()
        self.main=tk.Tk()
        self.main.title('主菜单')
        self.main.resizable(0,0)
        self.main.geometry('300x500+550+100')
        self.ctitle=tk.Label(self.main,font=('times',16),anchor='center',text='您好')
        self.ctitle.place(x=50,y=40,width=200,height=50)
        if(perinfo[1]):self.ctitle.config(text='您好，'+perinfo[1].rstrip())
        tk.Button(self.main,font=('times',12),anchor='center',text='个人信息',command=infor).place(x=70,y=100,width=160,height=60)
        tk.Button(self.main,font=('times',12),anchor='center',text='我的收藏',command=collect).place(x=70,y=170,width=160,height=60)
        tk.Button(self.main,font=('times',12),anchor='center',text='浏览市场',command=market).place(x=70,y=240,width=160,height=60)
        tk.Button(self.main,font=('times',12),anchor='center',text='我的物品',command=sell).place(x=70,y=310,width=160,height=60)
        tk.Button(self.main,font=('times',12),anchor='center',text='我的订单',command=purch).place(x=70,y=380,width=160,height=60)
class personalinfo():
    def __init__(self):
        def goaddr():
            addressmanage().main.transient()
        def modify():
            perinfo[1]=username.get()
            perinfo[2]=telephone.get()
            perinfo[3]=birthday.get()
            perinfo[5]=sex.get()
            if(perinfo[5]=='男'):perinfo[5]='1'
            elif(perinfo[5]=='女'):perinfo[5]='0'
            try:
                cur.execute('update Users set userName=%s,telephone=%s,birthday=%s,sex=%s where account=%s',(perinfo[1],perinfo[2],perinfo[3],perinfo[5],perinfo[0]))
                tradeinfo.commit()
            except:
                tradeinfo.rollback()
                tem.config(text='请检查输入')
                return
            tem.config(text='修改成功')
            global main
            main.ctitle.config(text='您好，'+perinfo[1].rstrip())
        cur.execute('select * from Users where account=%s',account)
        perinfo=list(cur.fetchone())
        self.main=tk.Toplevel()
        self.main.title('个人信息')
        self.main.resizable(0,0)
        self.main.geometry('500x350+600+90')
        tk.Label(self.main,font=('times',12),anchor='w',text='账号  '+perinfo[0].rstrip()).place(x=50,y=15,width=200,height=30)
        tk.Label(self.main,font=('times',12),anchor='e',text='用户名').place(x=7,y=50,width=80,height=30)
        username=tk.StringVar()
        tem=tk.Entry(self.main,font=('times',12),textvariable=username)
        tem.place(x=90,y=50,width=300,height=30)
        if(perinfo[1]):tem.insert('insert',perinfo[1].rstrip())
        tk.Label(self.main,font=('times',12),anchor='e',text='联系方式').place(x=7,y=85,width=80,height=30)
        telephone=tk.StringVar()
        tem=tk.Entry(self.main,font=('times',12),textvariable=telephone)
        tem.place(x=90,y=85,width=300,height=30)
        if(perinfo[2]):tem.insert('insert',perinfo[2].rstrip())
        tk.Label(self.main,font=('times',12),anchor='e',text='生日').place(x=7,y=120,width=80,height=30)
        birthday=tk.StringVar()
        tem=tk.Entry(self.main,font=('times',12),textvariable=birthday)
        tem.place(x=90,y=120,width=300,height=30)
        if(perinfo[3]):tem.insert('insert',str(perinfo[3]))
        tk.Label(self.main,font=('times',12),anchor='w',text='注册日期  '+str(perinfo[4])).place(x=17,y=155,width=200,height=30)
        tk.Label(self.main,font=('times',12),anchor='e',text='性别').place(x=7,y=190,width=80,height=30)
        sex=tk.StringVar()
        tem=tk.Entry(self.main,font=('times',12),textvariable=sex)
        tem.place(x=90,y=190,width=300,height=30)
        if(perinfo[5]!=None):
            if(perinfo[5]):tem.insert('insert','男')
            else:tem.insert('insert','女')
        tk.Label(self.main,font=('times',12),anchor='w',text='信用等级  '+str(perinfo[6])).place(x=17,y=225,width=200,height=30)
        tk.Label(self.main,font=('times',12),anchor='w',text='电子邮箱  '+perinfo[7].rstrip()).place(x=17,y=260,width=450,height=30)
        tk.Button(self.main,font=('times',12),anchor='center',text='地址管理',command=goaddr).place(x=20,y=295,width=70,height=30)
        tk.Button(self.main,font=("times",16),anchor='center',text='确认\n修改',command=modify).place(x=400,y=50,width=90,height=170)
        tem=tk.Label(self.main,font=('times',12),anchor='nw')
        tem.place(x=200,y=295,width=270,height=30)
class addressmanage():
    def __init__(self):
        def ins():
            addr=spaddress.get()
            if(not addr):
                notice.config(text='请输入地址')
                return
            try:
                cur.execute('insert into Address(account,specificAddress) values(%s,%s)',(perinfo[0],addr))
                tradeinfo.commit()
                notice.config(text='添加成功')
                addrlst.insert('end',addr)
                spaddress.set('')
            except:
                tradeinfo.rollback()
                notice.config(text='字段过长或与现有地址重复')
        def delet():
            addr=addrlst.get('active')
            try:
                cur.execute('delete from Address where account=%s and specificAddress=%s',(perinfo[0],addr))
                tradeinfo.commit()
                notice.config(text='删除成功')
                addrlst.delete('active')
            except:
                tradeinfo.rollback()
                notice.config(text='删除出错')
        def receive():
            addr=addrlst.get('active')
            cur.execute('update Users set receiveAddress=%s where account=%s',(addr,perinfo[0]))
            tradeinfo.commit()
            rec.config(text=addr)
            perinfo[8]=addr
        def shipping():
            addr=addrlst.get('active')
            cur.execute('update Users set shipAddress=%s where account=%s',(addr,perinfo[0]))
            tradeinfo.commit()
            ship.config(text=addr)
            perinfo[9]=addr
        self.main=tk.Toplevel()
        self.main.title('地址管理')
        self.main.resizable(0,0)
        self.main.geometry('600x480+500+150')
        addrlst=tk.Listbox(self.main,justify='left',font=('times',14))
        sc=tk.Scrollbar(addrlst,command=addrlst.yview)
        sc.pack(side='right',fill='y')
        addrlst.config(yscrollcommand=sc.set)
        cur.execute('select * from Address where account=%s',perinfo[0])
        for item in cur.fetchall():
            addrlst.insert('end',item[1].encode('latin1').decode('gbk').rstrip())
        addrlst.place(x=0,y=100,width=600,height=300)
        spaddress=tk.StringVar()
        tk.Entry(self.main,font=('times',12),textvariable=spaddress).place(x=50,y=30,width=400,height=30)
        tk.Button(self.main,font=('times',12),text='添加',command=ins).place(x=460,y=30,width=50,height=30)
        tk.Button(self.main,font=('times',12),text='删除',command=delet).place(x=520,y=30,width=50,height=30)
        notice=tk.Label(self.main,font=('times',12),anchor='w')
        notice.place(x=50,y=60,width=200,height=30)
        tk.Button(self.main,font=('times',12),text='收货',command=receive).place(x=10,y=410,width=50,height=30)
        tk.Button(self.main,font=('times',12),text='发货',command=shipping).place(x=310,y=410,width=50,height=30)
        rec=tk.Label(self.main,font=('times',12),anchor='w')
        try:perinfo[8]=perinfo[8].encode('latin1').decode('gbk')
        except:pass
        if(perinfo[8]):rec.config(text=perinfo[8])
        rec.place(x=10,y=440,width=290,height=30)
        try:perinfo[9]=perinfo[9].encode('latin1').decode('gbk')
        except:pass
        ship=tk.Label(self.main,font=('times',12),anchor='w',text=perinfo[9])
        ship.place(x=310,y=440,width=290,height=30)
class collectionpage():
    def __init__(self):
        def ins():
            code=gcode.get()
            if(not code):
                notice.config(text='请输入物品编号')
                return
            cur.execute('select goodsName from Goods where goodsNo=%s',code)
            tname=cur.fetchone()
            if(not tname):
                notice.config(text='物品不存在')
                return
            try:
                cur.execute('insert into Collections(account,goodsNo,collectDate) values(%s,%s,%s)',(perinfo[0],code,str(date.date.today())))
                tradeinfo.commit()
                notice.config(text='添加成功')
                collst.insert('end',code+' '*8+str(date.date.today())+' '*14+tname[0].encode('latin1').decode('gbk'))
                gcode.set('')
            except:
                tradeinfo.rollback()
                notice.config(text='已经添加过该物品')
        def delet():
            code=collst.get('active').split()[0]
            if(code=='物品编号'):return
            cur.execute('delete from Collections where account=%s and goodsNo=%s',(perinfo[0],code))
            tradeinfo.commit()
            collst.delete('active')
            notice.config(text='删除成功')
        self.main=tk.Toplevel()
        self.main.title('我的收藏')
        self.main.resizable(0,0)
        self.main.geometry('600x480+500+150')
        collst=tk.Listbox(self.main,justify='left',font=('times',14))
        sc=tk.Scrollbar(collst,command=collst.yview)
        sc.pack(side='right',fill='y')
        collst.config(yscrollcommand=sc.set)
        cur.execute('select Collections.goodsNo,collectDate,goodsName from Collections,Goods where Collections.account=%s and Goods.goodsNo=Collections.goodsNo',perinfo[0])
        collst.insert('end','物品编号'+' '*18+'收藏日期'+' '*15+'物品名称')
        for item in cur.fetchall():
            collst.insert('end',item[0]+' '*8+str(item[1])+' '*14+item[2].encode('latin1').decode('gbk').rstrip())
        collst.place(x=0,y=100,width=600,height=380)
        gcode=tk.StringVar()
        tk.Entry(self.main,font=('times',12),textvariable=gcode).place(x=50,y=30,width=400,height=30)
        tk.Button(self.main,font=('times',12),text='添加',command=ins).place(x=460,y=30,width=50,height=30)
        tk.Button(self.main,font=('times',12),text='删除',command=delet).place(x=520,y=30,width=50,height=30)
        notice=tk.Label(self.main,font=('times',12),anchor='w')
        notice.place(x=50,y=60,width=200,height=30)
class marketpage():
    def __init__(self):
        def purchase():
            def buy():
                tem=tar.get();info=goods.get('active').split()
                if(int(tem)>ct):
                    notice.config(text='库存不足！')
                    return
                cur.execute('select shipAddress from Users where account=%s',info[1])
                ship=cur.fetchone()[0].rstrip().encode('latin1').decode('gbk')
                try:
                    perinfo[8]=perinfo[8].rstrip().encode('latin1').decode('gbk')
                except:pass
                cur.execute('exec purchasing %s,%s,%s,%s,%s,%s,%s',(perinfo[0],info[0],tem,str(date.date.today()),randint(19),perinfo[8].rstrip(),ship))
                tradeinfo.commit()
                main.destroy()
            gcode=goods.get('active').split()[0]
            if(gcode=='物品编号'):return
            cur.execute('select goodsAmount from Goods where goodsNo=%s',gcode)
            ct=cur.fetchone()[0]
            main=tk.Toplevel()
            main.title('购买')
            main.resizable(0,0)
            main.geometry('400x80+600+300')
            tk.Label(main,font=('times',12),text='库存：'+str(ct)).place(x=125,y=0,width=150,height=30)
            tk.Label(main,font=('times',12),anchor='e',text='购买数量').place(x=0,y=40,width=95,height=30)
            tar=tk.StringVar()
            tk.Entry(main,font=('times',12),textvariable=tar).place(x=100,y=40,width=230,height=30)
            tk.Button(main,font=('times',12),text='确定',command=buy).place(x=340,y=40,width=50,height=30)
            notice=tk.Label(main,font=('times',12),anchor='w')
            notice.place(x=280,y=0,width=120,height=30)
            main.wait_window(main)
        def view():
            def pro():
                ct=comt.get('active').split()[2]
                if(ct=='赞同'):return
                cur.execute('update Comments set agree=%s where account=%s and goodsNo=%s',(str(int(ct)+1),perinfo[0],gn))
                tradeinfo.commit()
            def con():
                ct=comt.get('active').split()[3]
                if(ct=='异议'):return
                cur.execute('update Comments set disagree=%s where account=%s and goodsNo=%s',(str(int(ct)+1),perinfo[0],gn))
                tradeinfo.commit()
            gn=goods.get('active').split()[0]
            if(gn=='物品编号'):return
            main=tk.Toplevel()
            main.title('评价')
            main.resizable(0,0)
            main.geometry('600x480+550+200')
            comt=tk.Listbox(main,font=('times',14),justify='left')
            scx=tk.Scrollbar(comt,command=comt.xview,orient='horizontal')
            scx.pack(side='bottom',fill='x')
            scy=tk.Scrollbar(comt,command=comt.yview)
            scy.pack(side='right',fill='y')
            comt.config(yscrollcommand=scy.set,xscrollcommand=scx.set)
            cur.execute('select account,commentDate,commentContent,agree,disagree from Comments where goodsNo=%s and commentDate is not null',gn)
            comt.insert('end','账号'+' '*18+'评价日期'+' '*15+'赞同'+' '*3+'异议'+' '*3+'评价')
            for item in cur.fetchall():
                comt.insert('end',item[0]+' '*11+str(item[1])+' '*14+str(item[3])+' '*8+str(item[4])+' '*10+item[2].rstrip().encode('latin1').decode('gbk'))
            comt.place(x=0,y=0,width=600,height=400)
            tk.Button(main,font=('times',12),text='赞同',command=pro).place(x=180,y=425,width=50,height=30)
            tk.Button(main,font=('times',12),text='异议',command=con).place(x=330,y=425,width=50,height=30)
        def search():
            goods.delete(1,'end')
            key='%'+keyword.get()+'%'
            cur.execute('select goodsNo,account,goodsPrice,goodsName from Goods where goodsNo like %s or goodsName like %s',(key,key))
            tem=cur.fetchall()
            if(not tem):return
            for item in tem:
                goods.insert('end',item[0]+' '*8+item[1]+' '*17+str(item[2])+' '*19+item[3].rstrip().encode('latin1').decode('gbk')+' '*5)
        self.main=tk.Toplevel()
        self.main.title('市场')
        self.main.resizable(0,0)
        self.main.geometry('600x480+530+180')
        goods=tk.Listbox(self.main,font=('times',14),justify='left')
        scy=tk.Scrollbar(goods,command=goods.yview)
        scy.pack(side='right',fill='y')
        scx=tk.Scrollbar(goods,command=goods.xview,orient='horizontal')
        scx.pack(side='bottom',fill='x')
        goods.config(yscrollcommand=scy.set,xscrollcommand=scx.set)
        cur.execute('select goodsNo,account,goodsPrice,goodsName from Goods')
        goods.insert('end','物品编号'+' '*18+'所属账号'+' '*15+'物品价格'+' '*15+'物品名称')
        for item in cur.fetchall():
            goods.insert('end',item[0]+' '*8+item[1]+' '*17+str(item[2])+' '*19+item[3].rstrip().encode('latin1').decode('gbk')+' '*5)
        goods.place(x=0,y=0,width=600,height=400)
        tk.Button(self.main,font=('times',12),text='购买',command=purchase).place(x=300,y=425,width=50,height=30)
        tk.Button(self.main,font=('times',12),text='查看评价',command=view).place(x=400,y=425,width=100,height=30)
        keyword=tk.StringVar()
        tk.Entry(self.main,font=('times',12),textvariable=keyword).place(x=10,y=425,width=200,height=30)
        tk.Button(self.main,font=('times',12),text='搜索',command=search).place(x=220,y=425,width=50,height=30)
class sellgoods():
    def get_info(info):
        def confirm():
            info[1]=goodsname.get()
            info[2]=amount.get()
            info[3]=price.get()
            info[4]=tem.get(1.0,'end')
            if(not info[1] or not info[2] or not info[3]):
                notice.config(text='请完整录入信息')
                info[4]=''
                return
            if(not info[4]):info[4]=' '
            main.destroy()
        def cancel():
            main.destroy()
        main=tk.Toplevel()
        main.focus()
        main.title('确认信息')
        main.resizable(0,0)
        main.geometry('450x300+550+200')
        tk.Label(main,font=('times',12),anchor='w',text='物品编号  '+info[0]).place(x=17,y=15,width=200,height=30)
        goodsname=tk.StringVar()
        tk.Label(main,font=('times',12),anchor='e',text='物品名称').place(x=7,y=50,width=80,height=30)
        tem=tk.Entry(main,font=('times',12),textvariable=goodsname)
        tem.place(x=90,y=50,width=300,height=30)
        if(info[1]):tem.insert('insert',info[1].rstrip().encode('latin1').decode('gbk'))
        amount=tk.StringVar()
        tk.Label(main,font=('times',12),anchor='e',text='库存量').place(x=7,y=85,width=80,height=30)
        tem=tk.Entry(main,font=('times',12),textvariable=amount)
        tem.place(x=90,y=85,width=300,height=30)
        if(info[2]):tem.insert('insert',str(info[2]))
        price=tk.StringVar()
        tk.Label(main,font=('times',12),anchor='e',text='物品单价').place(x=7,y=120,width=80,height=30)
        tem=tk.Entry(main,font=('times',12),textvariable=price)
        tem.place(x=90,y=120,width=300,height=30)
        if(info[3]):tem.insert('insert',str(info[3]))
        tk.Label(main,font=('times',12),anchor='e',text='物品描述').place(x=7,y=155,width=80,height=30)
        tem=tk.Text(main,font=('times',12),wrap='char')
        tem.place(x=90,y=155,width=300,height=90)
        if(info[4]):
            tem.insert('insert',info[4].rstrip().encode('latin1').decode('gbk'))
            info[4]=''
        tk.Button(main,font=('times',12),text='确定',command=confirm).place(x=140,y=255,width=50,height=30)
        tk.Button(main,font=('times',12),text='取消',command=cancel).place(x=260,y=255,width=50,height=30)
        notice=tk.Label(main,font=('times',12),anchor='w')
        notice.place(x=250,y=15,width=200,height=30)
        main.wait_window(main)
        return info
    def __init__(self):
        def ins():
            info=sellgoods.get_info([randstr(10),'','','',''])
            if(not info[4]):return
            cur.execute('insert into Goods(goodsNo,account,goodsName,goodsAmount,goodsPrice,goodsDescription) values(%s,%s,%s,%s,%s,%s)',(info[0],perinfo[0],info[1],info[2],info[3],info[4]))
            tradeinfo.commit()
            goods.insert('end',info[0]+' '*8+info[3]+' '*22+info[1])
        def modify():
            info=goods.get('active').split()[0]
            if(info=='物品编号'):return
            cur.execute('select goodsNo,goodsName,goodsAmount,goodsPrice,goodsDescription from Goods where goodsNo=%s',info)
            info=sellgoods.get_info(list(cur.fetchone()))
            if(not info[4]):return
            cur.execute('update Goods set goodsName=%s,goodsAmount=%s,goodsPrice=%s,goodsDescription=%s where account=%s and goodsNo=%s',(info[1],info[2],info[3],info[4],perinfo[0],info[0]))
            tradeinfo.commit()
            goods.delete('active')
            goods.insert('end',info[0]+' '*8+info[3]+' '*22+info[1])
        def delet():
            info=goods.get('active').split()[0]
            if(info=='物品编号'):return
            cur.execute('select goodsNo,goodsName,goodsAmount,goodsPrice,goodsDescription from Goods where goodsNo=%s',info)
            info=sellgoods.get_info(list(cur.fetchone()))
            if(not info[4]):return
            cur.execute('delete from Goods where goodsNo=%s',info[0])
            tradeinfo.commit()
            goods.delete('active')
        self.main=tk.Toplevel()
        self.main.title('我的物品')
        self.main.resizable(0,0)
        self.main.geometry('600x480+500+150')
        goods=tk.Listbox(self.main,font=('times',14),justify='left')
        sc=tk.Scrollbar(goods,command=goods.yview)
        sc.pack(side='right',fill='y')
        goods.config(yscrollcommand=sc.set)
        cur.execute('select goodsNo,goodsPrice,goodsName from Goods where account=%s',perinfo[0])
        goods.insert('end','物品编号'+' '*18+'物品价格'+' '*15+'物品名称')
        for item in cur.fetchall():
            goods.insert('end',item[0]+' '*8+str(item[1])+' '*22+item[2].rstrip().encode('latin1').decode('gbk'))
        goods.place(x=0,y=0,width=600,height=400)
        tk.Button(self.main,font=('times',12),text='添加',command=ins).place(x=100,y=425,width=50,height=30)
        tk.Button(self.main,font=('times',12),text='修改',command=modify).place(x=270,y=425,width=50,height=30)
        tk.Button(self.main,font=('times',12),text='删除',command=delet).place(x=440,y=425,width=50,height=30)
class purchasemanage():
    def __init__(self):
        def show():
            slct=purch.get('active').split()[2]
            if(slct=='订单编号'):return
            main=tk.Toplevel()
            main.title('详细信息')
            main.resizable(0,0)
            main.geometry('350x300+600+300')
            cur.execute('select * from Logistics where purchaseNo=%s',slct)
            slct=cur.fetchone()
            tk.Label(main,font=('times',12),anchor='w',text='订单编号  '+slct[0]).place(x=50,y=15,width=300,height=30)
            tk.Label(main,font=('times',12),anchor='w',text='寄出地址  '+slct[2].rstrip().encode('latin1').decode('gbk')).place(x=50,y=50,width=300,height=30)
            tk.Label(main,font=('times',12),anchor='w',text='收货地址  '+slct[1].rstrip().encode('latin1').decode('gbk')).place(x=50,y=85,width=300,height=30)
            tk.Label(main,font=('times',12),anchor='w',text='物流状态  '+slct[3].rstrip().encode('latin1').decode('gbk')).place(x=50,y=120,width=300,height=30)
        def comment():
            def upd():
                cur.execute('update Comments set commentContent=%s,commentDate=%s where account=%s and goodsNo=%s',(tem.get(1.0,'end'),str(date.date.today()),perinfo[0],gn))
                tradeinfo.commit()
                main.destroy()
            gn=purch.get('active').split()[0]
            if(gn=='物品编号'):return
            main=tk.Toplevel()
            main.title('评价')
            main.resizable(0,0)
            main.geometry('350x300+650+350')
            cur.execute('select commentContent,commentDate from Comments where account=%s and goodsNo=%s',(perinfo[0],gn))
            hisinfo=cur.fetchone()
            tk.Label(main,font=('times',12),anchor='w',text='上一次评价时间：'+str(hisinfo[1])).place(x=45,y=15,width=250,height=30)
            tk.Label(main,font=('times',12),text='评价').place(x=0,y=50,width=350,height=30)
            tem=tk.Text(main,font=('times',12),wrap='char')
            tem.place(x=50,y=85,width=250,height=150)
            tem.insert('1.0',hisinfo[0].rstrip().encode('latin1').decode('gbk'))
            tk.Button(main,font=('times',12),text='确定',command=upd).place(x=150,y=250,width=50,height=30)
        self.main=tk.Toplevel()
        self.main.title('我的订单')
        self.main.resizable(0,0)
        self.main.geometry('600x480+500+150')
        purch=tk.Listbox(self.main,font=('times',14),justify='left')
        scy=tk.Scrollbar(purch,command=purch.yview)
        scy.pack(side='right',fill='y')
        scx=tk.Scrollbar(purch,command=purch.xview,orient='horizontal')
        scx.pack(side='bottom',fill='x')
        purch.config(yscrollcommand=scy.set,xscrollcommand=scx.set)
        cur.execute('select Purchase.goodsNo,purchaseDate,purchaseNo,goodsName from Purchase,Goods where Purchase.account=%s and Goods.goodsNo=Purchase.goodsNo',perinfo[0])
        purch.insert('end','物品编号'+' '*18+'购买日期'+' '*18+'订单编号'+' '*25+'物品名称')
        for item in cur.fetchall():
            purch.insert('end',item[0]+' '*8+str(item[1])+' '*17+item[2]+' '*5+item[3].rstrip().encode('latin1').decode('gbk')+' '*5)
        purch.place(x=0,y=0,width=600,height=400)
        tk.Button(self.main,font=('times',12),text='物流信息',command=show).place(x=150,y=425,width=100,height=30)
        tk.Button(self.main,font=('times',12),text='评价',command=comment).place(x=360,y=425,width=50,height=30)
tradeinfo=ssms.connect(host='localhost',database='tradeinfo')
cur=tradeinfo.cursor()
account='00000000'
login().main.mainloop()#
tradeinfo.close();cur.close()
if(not account):exit(0)
#
tradeinfo=ssms.connect(host='localhost',user='user01',password='P88888888',database='tradeinfo')
cur=tradeinfo.cursor()
cur.execute('select * from Users where account=%s',account)
perinfo=list(cur.fetchone())
main=menupage()
main.main.mainloop()
tradeinfo.close();cur.close()