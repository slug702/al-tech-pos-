#import PIL
import tkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox
#from PIL import ImageTk, Image
from tkinter import ttk, LabelFrame, StringVar
from tkinter import ttk, LabelFrame, StringVar
#from PIL import ImageDraw
import tkinter.messagebox
import sqlite3
import functools
import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta
import re
#from PyTouchBar import TouchBarItems

global vat
vat = "12"
global tinvid
tinvid = ''
#idea house
#pos #1
#CASHIER SIDE
#get VAT from other records table
#GUI
top = tk.Tk()
style = ttk.Style(top)
top.tk.call('source', 'azure.tcl')
style.theme_use('azure')
d = StringVar()
d.set('no-disc')
invd = StringVar()
invd.set('no-disc')
global t1
t1 = StringVar()
t1.set('')
t2 = StringVar()
t2.set('')
global inv1
global tid1
global mop1
mop1 = StringVar()
cashinsrt = StringVar()
tid1 = ''
inv1 = StringVar()
global orders
orders = []


#-- date today --
idate1 = str(datetime.today()).split()[0]
conn = sqlite3.connect('res.db')


c = conn.cursor()



#c.execute("CREATE TABLE invoices (iid INTEGER PRIMARY KEY, idate DATE, iproducts TEXT, mop TEXT, tprce INTEGER, pbd INTEGER, idscnt INTEGER, vat INTEGER, paid INTEGER, change INTEGER, status TEXT, cashier TEXT)")

#treeview for table orders
tabletrv = ttk.Treeview(top, column=(1, 2, 3), show="headings", height="34")
style = ttk.Style(tabletrv)
tabletrv.heading(1, text="Item")
tabletrv.column(1, width=400)
tabletrv.heading(2, text="Price")
tabletrv.column(2, width=120+10+4)
tabletrv.heading(3, text="Discount")
tabletrv.column(3, width=120+10+4)
tabletrv.place(x=450, y=65)

#display active invoices in combo box
def grabinv():
    global tablelist
    tablelist = []
    query = "SELECT iid from invoices WHERE status = ?"
    c.execute(query, ("active",))
    invnum = c.fetchall()
    for i in invnum:
        tablelist.append(str(i[0]))
    return

grabinv()
#selecting invoice from combo box
def selectinv(event):

    global inv1
    inv1 = StringVar()
    inv1.set(tables.get())
    #new
    global tinvid
    grabinv()
    tables['values'] = tablelist
    tinvid = inv1.get()
    #print(tinvid)
    query = "SELECT trdesc, trprce, dscnt, tid from transactions WHERE invid = ?"
    c.execute(query, (inv1.get(),))
    iitems = c.fetchall()
    #print(iitems)
    tabletrv.delete(*tabletrv.get_children())
    for i in iitems:
        tabletrv.insert("", 'end', values=i)
    #print(inv1.get())
    return
#combo box for invoices
tables = ttk.Combobox(top, values=tablelist, width=12)
tables.current()
tables.set('Select Table')
tables.place(x=450+200+159+118, y=20)
tables.bind("<<ComboboxSelected>>", selectinv)


#treeview for products/menu items
menutrv = ttk.Treeview(top, column=(1, 2), show="headings", height="34")
style = ttk.Style(menutrv)
menutrv.heading(1, text="Item")
menutrv.column(1, width=300, anchor=N)
menutrv.heading(2, text="Price")
menutrv.column(2, width=80, anchor=N)
menutrv.place(x=10, y=65)

#data for items in the menu
def itemquery():
    c.execute("SELECT desc, price, pid from products")
    items = c.fetchall()
    menutrv.delete(*menutrv.get_children())
    for i in items:
        menutrv.insert("", 'end', values=i)
    return
itemquery()
#grab data for orders
def getorderdata():
    query = "SELECT trdesc, trprce, dscnt, tid from transactions WHERE invid = ?"
    c.execute(query, (inv1.get(),))
    iitems = c.fetchall()
    tabletrv.delete(*tabletrv.get_children())
    for i in iitems:
        tabletrv.insert("", 'end', values=i)

    return
def dispitems():

    if tinvid == '':
        return
    else:
        getorderdata()




itemquery()


#select menu id
def getrows(event):
    rowid = menutrv.identify_row(event.y)
    newitem = menutrv.item(menutrv.focus())
    t1.set(newitem['values'][2])
    global pid
    pid = t1.get()
#select order id
def getrowsorder(event):
    rowid1 = tabletrv.identify_row(event.y)
    delorder = tabletrv.item(tabletrv.focus())
    t2.set(delorder['values'][3])
    global tid1
    tid1 = t2.get()
# add item
def additem():
    if tinvid == '':
        messagebox.showerror('Error!', 'Create An Active Table First!')
        return

    #get item info from invoices (create the list in invoice button)
    if t1.get() == '':
        messagebox.showerror('Error!', 'Select A Menu Item First!')
        return
    productid = int(t1.get())
    pid = t1.get()
    query1 = ("SELECT desc from products WHERE pid = ?")
    c.execute(query1, (pid,))
    item = c.fetchone()
    query2 = ("SELECT price from products WHERE pid = ?")
    c.execute(query2, (pid,))
    prce = c.fetchone()
    itm = item[0]
    prce1 = prce[0]
    dsc = int('0')
    dscntcalprce = int(prce1)
    calprice = int(prce1)

    def insert():

        c.execute("INSERT INTO transactions VALUES (:tid, :trprid, :trdesc, :trprce, :dscnt, :invid)",
                  {

                      'tid': None,
                      'trprid': productid,
                      'trdesc': itm,
                      'trprce': calprice,
                      'dscnt': dsc,
                      'invid': inv1.get(),
                  })
        conn.commit()
        getorderdata()
    if d.get() == 'disc':
        global adddscnt
        def adddscnt():
            try:
                int(disc1.get())
            except ValueError:
                tkinter.messagebox.showerror("Error!", "Please Enter Integer!")
                return
            dscnt = int(disc1.get())
            hundo = int("100")
            times = float(dscnt/hundo)
            dscntcalprce = float(prce1)
            stepprice = float(dscntcalprce*times)
            calprice = int(stepprice)
            csprice = int(dscntcalprce - stepprice)
            #print(calprice)
            c.execute("INSERT INTO transactions VALUES (:tid, :trprid, :trdesc, :trprce, :dscnt, :invid)",
                      {

                          'tid': None,
                          'trprid': productid,
                          'trdesc': itm,
                          'trprce': csprice,
                          'dscnt': dscnt,
                          'invid': inv1.get(),
                      })
            conn.commit()
            orders.append(itm)
            adddisc.destroy()
            getorderdata()
        adddisc = Toplevel()
        adddisc.geometry("500x500")
        disc1 = ttk.Entry(adddisc , width=10)
        disc1.place(x=250 - 40, y=150)
        discbtn = ttk.Button(adddisc , text="Add Item With Discount", command=adddscnt)
        discbtn.place(x=180, y=200)

        #-------ORDERS LIST IS WHAT U INSERT INTO INVOICE, NOT TRANSACTION------
        #-------ADD PID FIELD TO TRANSACTIONS--------------

    else:
        insert()

def deleteitem():
    if tinvid == '':
        messagebox.showerror('Error!', 'Create An Active Table First!')
        return
    if tid1 == '':
        messagebox.showerror('Error!', 'Please Select An Order to Delete!')
        return
    query = "DELETE FROM transactions WHERE tid = ?"
    c.execute(query, (tid1, ))
    query = "SELECT trdesc, trprce, dscnt, tid from transactions WHERE invid = ?"
    c.execute(query, (inv1.get(),))
    iitems = c.fetchall()
    tabletrv.delete(*tabletrv.get_children())
    for i in iitems:
        tabletrv.insert("", 'end', values=i)

    return
#create new invoice -- for button
def newinv():
    tablestat1.config(text="Active Table", font='{Courier New} 25')
    selcas()

    global itm
    itm = [None]
    return
def insertinv():
    c.execute("INSERT INTO invoices VALUES (:iid, :idate, :iproducts, :mop, :tprce, :pbd, :idscnt, :vat, :paid, :change, :status, :cashier)",
            {

                'iid': None,
                'idate': idate1,
                'iproducts': None,
                'mop': None,
                'tprce': None,
                'pbd': None,
                'idscnt': None,
                'vat': None,
                'paid': None,
                'change': None,
                'status': "active",
                'cashier': cashinsrt.get(),
            }).lastrowid

    global tinvid
    tinvid = c.lastrowid
    tables.set(tinvid)
    grabinv()
    tables['values'] = tablelist
    #newinv()
    inv1.set(tinvid)
    getorderdata()
    conn.commit()
    return
#select cashier
def selcas():
        cashiers = ['Cashier 1', 'Cashier 2', 'Cashier 3,' 'Cashier 4']
        def selectcsh(event):
            global cashinsrt
            cashinsrt.set(cashier1.get())
            insertinv()
            csher.destroy()


        csher = Toplevel()
        csher.geometry('250x150')
        cashier1 = ttk.Combobox(csher, values=cashiers, width=12)
        cashier1.current(0)
        cashier1.set('Select Cashier')
        cashier1.place(x=150 - 90, y=40)
        cashier1.bind("<<ComboboxSelected>>", selectcsh)


def tableout():
    #GET ORDERS FOR INVOICE -- ordins
    global orderlist
    orderlist = []
    query = "SELECT trdesc from transactions WHERE invid = ?"
    c.execute(query, (inv1.get(),))
    invnum1 = c.fetchall()
    for i in invnum1:
        orderlist.append(str(i[0]))
    ordins = (', ').join(orderlist)

    c.execute("""UPDATE invoices SET iproducts = :ip WHERE iid = :id1""",
              {
                  'ip': ordins,
                  'id1': inv1.get()
              })
    conn.commit()
    #GET PRICE BEFORE DISCOUNT -- priceq1
    c.execute("SELECT SUM (trprce) FROM transactions WHERE invid =" + inv1.get())

    priceq = c.fetchone()
    priceq1 = int(priceq[0])

    c.execute("""UPDATE invoices SET pbd = :pbd1 WHERE iid = :id1""",
              {
                  'pbd1': priceq1,
                  'id1': inv1.get()
              })
    conn.commit()
    #UPDATE EACH COLUMN ----- TO DO LIST

    if invd.get() == "disc":
    #STAGES
        def adddscntinv():
            try:
                int(invdsc.get())
            except ValueError:
                tkinter.messagebox.showerror("Error!", "Please Enter Integer!")
                return
            dscnt2 = int(invdsc.get())
            hundo = int("100")
            times = float(dscnt2/hundo)
            priceq2 = float(priceq1)
            final = float(priceq2*times)
            discprce = int(final)
            #UPDATE DISCOUNT PIRCE
            nxt1 = Toplevel()
            nxt1.geometry("500x500")
            moplist = ['Cash', 'Card', 'Check']
            #MODE OF PAYMENT
            def selectmop(event):
                mop1.set(nx.get())
            nx = ttk.Combobox(nx1, values=moplist, width=12)
            nx.current(0)
            nx.set('Select MOP')
            nx.place(x=250 -40, y=150)
            nx.bind("<<ComboboxSelected>>", selectmop)
            def payment():

                if mop1.get() == 'Cash':
                    pay = Toplevel()
                    pay.geometry("500x500")
                #else:


            mopbtn = ttk.Button(nxt1, text="Next", command=payment)
            mopbtn.place(x=220, y=200)

            return
        invoicedisc = Toplevel()
        invoicedisc.geometry("500x500")
        invdsc = ttk.Entry(invoicedisc, width=10)
        invdsc.place(x=250 - 40, y=150)
        discinv = ttk.Button(invoicedisc, text="Next", command=adddscntinv)
        discinv.place(x=220, y=200)

    #GET MOP

    #GET CHANGE

    #VAT RATE

    return



menutrv.bind('<Double 1>', getrows)
tabletrv.bind('<Double 1>', getrowsorder)


additem = ttk.Button(top, text="Add Item", command=additem)
additem.place(x=450, y=20)

dscnt = ttk.Checkbutton(top, text="Add Discount", variable=d, onvalue="disc", offvalue="no-disc")
dscnt.place(x=450+120, y=22)
delitem = ttk.Button(top, text="Delete Item", command=deleteitem)
delitem.place(x=450+118+100+22, y=20)


newcust = ttk.Button(top, text="New Table", command=newinv)
newcust.place(x=650+200+200+4, y=20)

ttl = ttk.Label(top, text="Total: 0", font='{Courier New} 30')
ttl.place(x=1188, y=740-45)
tablestat1 = ttk.Label(top, text="No Table Active", font='{Courier New} 25')
tablestat1.place(x=1188, y=20)

out = ttk.Button(top, text="Table Out", width=10, style="AccentButton", command=tableout)
out.place(x=1188, y=780-45)
idscnt = ttk.Checkbutton(top, text="Add Discount", variable=invd, onvalue="disc", offvalue="no-disc")
idscnt.place(x=450+400+400+60, y=780-43)
rcpts = ttk.Button(top, text="See Past Invoices", width=24, style="AccentButton")
rcpts.place(x=1188, y=780-45+45)







top.title("V1")
top.geometry("1500x1200")
#icon photo
#top.tk.call('wm', 'iconphoto', top._w, tk.PhotoImage(file='yeah.png'))

top.mainloop()
