from tkinter import *
from tkinter import messagebox
import random
import time
import json
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.scard import (
    SCardEstablishContext, SCardListReaders, SCardConnect, SCardTransmit,
    SCardGetErrorMessage, SCARD_S_SUCCESS, SCARD_SCOPE_USER,
    SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0, SCARD_PROTOCOL_T1
)
from ftplib import FTP
import datetime
import os

def connect_ftp_server(ip, user, passwd):
    ftp = FTP(ip)
    ftp.login(user=user, passwd=passwd)
    return ftp

def download_file(ftp, filename):
    with open(filename, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)

def upload_file(ftp, filename):
    with open(filename, 'rb') as f:
        ftp.storbinary('STOR ' + filename, f)

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file does not exist")
        
# กำหนดข้อมูลสำหรับเชื่อมต่อ FTP server
ip = '10.64.194.31'
user = 'NetPro'
passwd = '123456'
filename = 'card_data.json'

ftp = connect_ftp_server(ip, user, passwd)
download_file(ftp, filename)

with open('menu1_data.json', 'r' , encoding='utf-8') as file:
    menu_data = json.load(file)

coffee_menu = menu_data['coffee_menu']
cake_menu = menu_data['cake_menu']

root = Tk()
root.geometry("1495x800+0+0")
root.title("Coffee Cafe")
root.configure(background='#333333')

Tops = Frame(root,width= 1350,height = 100, bd=14, relief="raise")
Tops.pack(side=TOP)


fMainL = Frame(root,width= 900,height = 650, bd=8, relief="raise")
fMainL.pack(side=LEFT)

fMainR = Frame(root,width= 440,height = 650, bd=8, relief="raise")
fMainR.pack(side=RIGHT)

fMLT = Frame(fMainL,width= 900,height = 320, bd=8, relief="raise")
fMLT.pack(side=TOP)

fMLB = Frame(fMainL,width= 900,height = 320, bd=6, relief="raise")
fMLB.pack(side=BOTTOM)

fReceipt = Frame(fMainR,width= 440,height = 450, bd=12, relief="raise")
fReceipt.pack(side=TOP)
fButton = Frame(fMainR,width= 440,height = 240, bd=12, relief="raise")
fButton.pack(side=BOTTOM)

fButton2 = Frame(fMainR,width= 440,height = 240, bd=12, relief="raise")
fButton2.pack(side=BOTTOM)

fDrink = Frame(fMLT,width= 400,height =
                330, bd=16, relief="raise")
fDrink.pack(side=LEFT)
fCake = Frame(fMLT,width= 400,height = 320, bd=16, relief="raise")
fCake.pack(side=RIGHT)

fCost1 = Frame(fMLB,width= 440,height = 330, bd=14, relief="raise")
fCost1.pack(side=LEFT)
fCost2 = Frame(fMLB,width= 440,height = 320, bd=14, relief="raise")
fCost2.pack(side=RIGHT)

Tops.configure(background='#FADBD8')
fMainL.configure(background='#333333')
fMainR.configure(background='#333333')

lblInfo = Label(Tops,font=('Adobe Hebrew',60,'bold'),text = "Coffee Cafe",bg="#FADBD8",bd=10)
lblInfo.grid(row=0,column=0)  

#============================= Function =====================
def qExit():
    qExit= messagebox.askyesno("Quit System!!!", "Do you want to quit?")
    if qExit > 0:
        root.destroy()
        return
def Reset():
    FrameDrinkReset()
    FrameCakeReset()
    FrameCostReset()
    txtReceipt.delete("1.0",END)

def FrameDrinkReset():
    for x in VarDrinkList:    
        x.set("0")

    for x in EntryDrinkList:    
        x.set("0")

    txtDrink0.configure(state = DISABLED)
    txtDrink1.configure(state = DISABLED)
    txtDrink2.configure(state = DISABLED)
    txtDrink3.configure(state = DISABLED)
    txtDrink4.configure(state = DISABLED)
    txtDrink5.configure(state = DISABLED)
    txtDrink6.configure(state = DISABLED)
    txtDrink7.configure(state = DISABLED)

def FrameCakeReset():
    for x in VarCakeList:    
        x.set("0")

    for x in EntryCakeList:    
        x.set("0")

    txtCake0.configure(state = DISABLED)
    txtCake1.configure(state = DISABLED)
    txtCake2.configure(state = DISABLED)
    txtCake3.configure(state = DISABLED)
    txtCake4.configure(state = DISABLED)
    txtCake5.configure(state = DISABLED)
    txtCake6.configure(state = DISABLED)
    txtCake7.configure(state = DISABLED)
    
def FrameCostReset():
    CostofDrinks.set("")
    CostofCakes.set("")
    ServiceCharge.set("")
    PaidTax.set("")
    SubTotal.set("")
    TotalCost.set("")
    CostofDrinks.set("")
    CostofCakes.set("")
                 
def chkbutton_value(chkValue,txtLabel,Entry):
    if chkValue.get() == 1:
        txtLabel.configure(state=NORMAL)
    elif chkValue.get() == 0:
        txtLabel.configure(state=DISABLED)
        Entry.set("0")

def CostofItem():    
  
       TotalDrinkCost = 0
       TotalCakeCost = 0
       
       CakePriceList = [50,50,50,50,50,50,50,50]
       DrinkPriceList = [50,50,50,50,50,50,50,50]

       
       for i in range(8) :
             TotalDrinkCost += int(EntryDrinkList[i].get())* float(DrinkPriceList[i])
                                                             
       for i in range(8) :
             TotalCakeCost += int(EntryCakeList[i].get())* float(CakePriceList[i])

       DrinksPrice = "B", str('%.2f'%(TotalDrinkCost))
       CakesPrice = "B", str('%.2f'%(TotalCakeCost))
       CostofDrinks.set(DrinksPrice)
       CostofCakes.set(CakesPrice)
       SC = "B", str('%.2f'%(1.59))
       ServiceCharge.set(SC)

       CostPlus = TotalDrinkCost + TotalCakeCost + 1.59
        
       SubTotalofItems = "B", str('%.2f'%(CostPlus))
       SubTotal.set(SubTotalofItems)

       Tax = "B" , str('%.2f'%(CostPlus*0.07))
       PaidTax.set(Tax)
       TT = CostPlus * 0.07
       TC = "B" , str('%.2f'%(CostPlus + TT))
       TotalCost.set(TC)
       global totalPrice
       totalPrice = CostPlus + TT
def Receipt():
    txtReceipt.delete("1.0",END)
    x = random.randint(10908,500876)
    Point = totalPrice // 100
    randomRef = str(x)
    ReceiptRef.set("BILL"+randomRef)

    txtReceipt.insert(END,'Receipt Ref:\t\t\t'+ ReceiptRef.get()  + '\t\t' + DateofOrder.get() + "\n")
    txtReceipt.insert(END,'Items\t\t\t\t\t'+ 'Cost of Items \n\n')
      
    for i in range(8) :
        if int(EntryDrinkList[i].get()) > 0 :
            txtReceipt.insert(END, coffee_menu[i]['name'] +'\t\t\t\t\t'+ EntryDrinkList[i].get() + '\n')  
    
    for i in range(8) :
        if int(EntryCakeList[i].get()) > 0 :
            txtReceipt.insert(END, cake_menu[i]['name'] +'\t\t\t\t\t'+ EntryCakeList[i].get() + '\n')        

    txtReceipt.insert(END,'\nCost of Drinks : \t\t'+ CostofDrinks.get() + '\n')
    txtReceipt.insert(END,'Cost of Cakes : \t\t'+ CostofCakes.get() + '\n')
    txtReceipt.insert(END,'Service Charge : \t\t'+ ServiceCharge.get() + '\n')
    txtReceipt.insert(END,'Paid Tax : \t\t'+ PaidTax.get() + '\n')
    txtReceipt.insert(END,'Sub Total : \t\t'+ SubTotal.get() + '\n')
    txtReceipt.insert(END,'Total : \t\t'+ TotalCost.get() + '\n')
    txtReceipt.insert(END,'Total Price : \t\t'+ str('%.2f'%(totalPrice)) + '\n')
    txtReceipt.insert(END,'Point : \t\t'+ str(Point) + '\n')

def get_card_uid():
        try:
            # Establish a context with the system
            hresult, context = SCardEstablishContext(SCARD_SCOPE_USER)
            if hresult != SCARD_S_SUCCESS:
                print("Failed to establish context:", SCardGetErrorMessage(hresult))
                return None
                
            # Obtain the list of readers
            hresult, readers = SCardListReaders(context, [])
            if hresult != SCARD_S_SUCCESS:
                print("Failed to list readers:", SCardGetErrorMessage(hresult))
                return None
            
            if readers:
                reader = readers[0]  # Using the first available reader
                hresult, hcard, dwActiveProtocol = SCardConnect(context, reader, SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
                if hresult != SCARD_S_SUCCESS:
                    print("Failed to connect to the card:", SCardGetErrorMessage(hresult))
                    return None

                # Command to retrieve the UID. This might need adjustment for different cards.
                command = [0xFF,0xCA,0x00,0x00,0x04]
                hresult, response = SCardTransmit(hcard, dwActiveProtocol, command)
                if hresult == SCARD_S_SUCCESS:
                    uid = ''.join(['%02X' % b for b in response[:-2]])  # Excluding the status word
                    return uid
                else:
                    print("Failed to retrieve card UID:", SCardGetErrorMessage(hresult))
            else:
                print("No smart card readers found")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

# ฟังก์ชันสำหรับดำเนินการการชำระเงินด้วยบัตร
def Paywithcard():
    uid = get_card_uid()
    if uid is None:
        print("UID ของบัตรไม่สามารถอ่านได้")
        messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถอ่าน UID ของบัตรได้")
        return

    try:
        with open('card_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("ข้อผิดพลาด", "ไม่พบไฟล์ฐานข้อมูล")
        return

    user = next((item for item in data if item['uid'] == uid), None)
    if user is None:
        messagebox.showerror("ข้อผิดพลาด", "ไม่พบ UID ของบัตรในฐานข้อมูล")
        return

    new_balance = user['balance'] - totalPrice
    if new_balance < 0:
        messagebox.showerror("ข้อผิดพลาด", "ยอดเงินไม่เพียงพอ")
        return

    user['balance'] = new_balance
    pointCal = int(totalPrice // 100)
    user['points'] = user.get('points', 0) + int(totalPrice // 100)
    user['history'].append({'amount': totalPrice, 'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'type': 'pay', 'service': 'store1', 'point': pointCal})

    try:
        with open('card_data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        messagebox.showinfo("สำเร็จ", "ดำเนินการชำระเงินเรียบร้อยแล้ว!")
        upload_file(ftp, filename)
    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดขณะบันทึกข้อมูล: {str(e)}")

#====================== Variable Coffee =====================
ReceiptRef = StringVar()
DateofOrder = StringVar()
DateofOrder.set(time.strftime("%d/%m/%Y"))

#====================== Variable Cake =====================
# DrinkList = ["Lattae","Espresso","IceLattae","ValeCoffee","Cappuccino","AfricanCoffee","AmericanCoffee","IcedCappuccino"]

VarDrink0 = IntVar()
VarDrink1 = IntVar()
VarDrink2 = IntVar()
VarDrink3 = IntVar()
VarDrink4 = IntVar()
VarDrink5 = IntVar()
VarDrink6 = IntVar()
VarDrink7 = IntVar()

VarDrinkList = [VarDrink0,VarDrink1,VarDrink2,VarDrink3,VarDrink4,VarDrink5,VarDrink6,VarDrink7]

for x in VarDrinkList:    
    x.set("0")


EntryDrink0 = StringVar()
EntryDrink1 = StringVar()
EntryDrink2 = StringVar()
EntryDrink3 = StringVar()
EntryDrink4 = StringVar()
EntryDrink5 = StringVar()
EntryDrink6 = StringVar()
EntryDrink7 = StringVar()

EntryDrinkList = [EntryDrink0,EntryDrink1,EntryDrink2,EntryDrink3,EntryDrink4,EntryDrink5,EntryDrink6,EntryDrink7]

for x in EntryDrinkList:
    x.set("0")

#====================== Variable Cake =====================

CakeList = ["Coffee Cake","Red Velvet Cake","Black Forest Cake","Boston Cream Cake",
            "Lagos Chocolate","Kilburn Chocolate Cake","Carton Hill Cake","Queen Park Cake"]

VarCake0 = IntVar()
VarCake1 = IntVar()
VarCake2 = IntVar()
VarCake3 = IntVar()
VarCake4 = IntVar()
VarCake5 = IntVar()
VarCake6 = IntVar()
VarCake7 = IntVar()


VarCakeList = [VarCake0,VarCake1,VarCake2,VarCake3,
               VarCake4,VarCake5,VarCake6,VarCake7]

for x in VarCakeList:    
    x.set("0")

EntryCake0 = StringVar()
EntryCake1 = StringVar()
EntryCake2 = StringVar()
EntryCake3 = StringVar()
EntryCake4 = StringVar()
EntryCake5 = StringVar()
EntryCake6 = StringVar()
EntryCake7 = StringVar()


EntryCakeList = [EntryCake0,EntryCake1,EntryCake2,EntryCake3,
                 EntryCake4,EntryCake5,EntryCake6,EntryCake7]

for x in EntryCakeList:    
    x.set("0")
#===============================Variable Calculation =====================
PaidTax = StringVar()
SubTotal = StringVar()
TotalCost = StringVar()
CostofDrinks = StringVar()
CostofCakes = StringVar()
ServiceCharge = StringVar()

#==================================== Drink =================================

_ = Checkbutton(fDrink, text=str(coffee_menu[0]['name'])+' '+str(coffee_menu[0]['price']),variable = VarDrinkList[0],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarDrinkList[0],txtDrink0,EntryDrinkList[0])).grid(row= 0, sticky=W)
_ = Checkbutton(fDrink, text=str(coffee_menu[1]['name'])+' '+str(coffee_menu[1]['price']),variable = VarDrinkList[1],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarDrinkList[1],txtDrink1,EntryDrinkList[1])).grid(row= 1, sticky=W)
_ = Checkbutton(fDrink, text=str(coffee_menu[2]['name'])+' '+str(coffee_menu[2]['price']),variable = VarDrinkList[2],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarDrinkList[2],txtDrink2,EntryDrinkList[2])).grid(row= 2, sticky=W)
_ = Checkbutton(fDrink, text=str(coffee_menu[3]['name'])+' '+str(coffee_menu[3]['price']),variable = VarDrinkList[3],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarDrinkList[3],txtDrink3,EntryDrinkList[3])).grid(row= 3, sticky=W)
_ = Checkbutton(fDrink, text=str(coffee_menu[4]['name'])+' '+str(coffee_menu[4]['price']),variable = VarDrinkList[4],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarDrinkList[4],txtDrink4,EntryDrinkList[4])).grid(row= 4, sticky=W)
_ = Checkbutton(fDrink, text=str(coffee_menu[5]['name'])+' '+str(coffee_menu[5]['price']),variable = VarDrinkList[5],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarDrinkList[5],txtDrink5,EntryDrinkList[5])).grid(row= 5, sticky=W)
_ = Checkbutton(fDrink, text=str(coffee_menu[6]['name'])+' '+str(coffee_menu[6]['price']),variable = VarDrinkList[6],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarDrinkList[6],txtDrink6,EntryDrinkList[6])).grid(row= 6, sticky=W)
_ = Checkbutton(fDrink, text=str(coffee_menu[7]['name'])+' '+str(coffee_menu[7]['price']),variable = VarDrinkList[7],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarDrinkList[7],txtDrink7,EntryDrinkList[7])).grid(row= 7, sticky=W)


#=======================Enter Widgets for Drink=======================
#เนื่องจากต้องมีการเปลี่ยนค่า state เป็น Disable/Normal จึงต้องมีการใช้ชื่อตัวแปร 
txtDrink0 = Entry(fDrink,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryDrinkList[0],state = DISABLED)
txtDrink0.grid(row=0,column =1)
txtDrink1 = Entry(fDrink,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryDrinkList[1],state = DISABLED)
txtDrink1.grid(row=1,column =1)
txtDrink2 = Entry(fDrink,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryDrinkList[2],state = DISABLED)
txtDrink2.grid(row=2,column =1)
txtDrink3 = Entry(fDrink,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryDrinkList[3],state = DISABLED)
txtDrink3.grid(row=3,column =1)
txtDrink4 = Entry(fDrink,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryDrinkList[4],state = DISABLED)
txtDrink4.grid(row=4,column =1)
txtDrink5 = Entry(fDrink,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryDrinkList[5],state = DISABLED)
txtDrink5.grid(row=5,column =1)
txtDrink6 = Entry(fDrink,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryDrinkList[6],state = DISABLED)
txtDrink6.grid(row=6,column =1)
txtDrink7 = Entry(fDrink,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryDrinkList[7],state = DISABLED)
txtDrink7.grid(row=7,column =1)
#====================================== Cake====================================

"""CoffeeCake = Checkbutton(fCake, text="Coffee Cake \t",variable = var9,onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold')).grid(row= 0, column=0)"""    
_ = Checkbutton(fCake, text=str(cake_menu[0]['name'])+' '+str(cake_menu[0]['price']),variable = VarCakeList[0] ,onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarCakeList[0],txtCake0,EntryCakeList[0])).grid(row= 0, sticky=W)
_ = Checkbutton(fCake, text=str(cake_menu[1]['name'])+' '+str(cake_menu[1]['price']),variable = VarCakeList[1],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarCakeList[1],txtCake1,EntryCakeList[1])).grid(row= 1, sticky=W)

_ = Checkbutton(fCake, text=str(cake_menu[2]['name'])+' '+str(cake_menu[2]['price']),variable = VarCakeList[2],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarCakeList[2],txtCake2,EntryCakeList[2])).grid(row= 2, sticky=W)

_ = Checkbutton(fCake, text=str(cake_menu[3]['name'])+' '+str(cake_menu[3]['price']),variable = VarCakeList[3],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarCakeList[3],txtCake3,EntryCakeList[3])).grid(row= 3, sticky=W)

_ = Checkbutton(fCake, text=str(cake_menu[4]['name'])+' '+str(cake_menu[4]['price']),variable = VarCakeList[4],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarCakeList[4],txtCake4,EntryCakeList[4])).grid(row= 4, sticky=W)

_ = Checkbutton(fCake, text=str(cake_menu[5]['name'])+' '+str(cake_menu[5]['price']),variable = VarCakeList[5],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarCakeList[5],txtCake5,EntryCakeList[5])).grid(row= 5, sticky=W)

_ = Checkbutton(fCake, text=str(cake_menu[6]['name'])+' '+str(cake_menu[6]['price']),variable = VarCakeList[6],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarCakeList[6],txtCake6,EntryCakeList[6])).grid(row= 6, sticky=W)
_ = Checkbutton(fCake, text=str(cake_menu[7]['name'])+' '+str(cake_menu[7]['price']),variable = VarCakeList[7],onvalue = 1, offvalue=0,
                    font=('Adobe Hebrew',18,'bold'),command=lambda:chkbutton_value(VarCakeList[7],txtCake7,EntryCakeList[7])).grid(row= 7, sticky=W)

#=======================Enter Widgets for Cake =======================
#เนื่องจากต้องมีการเปลี่ยนค่า state เป็น Disable/Normal จึงต้องมีการใช้ชื่อตัวแปร   
txtCake0 = Entry(fCake,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryCakeList[0],state = DISABLED)
txtCake0.grid(row=0,column =1)
txtCake1 = Entry(fCake,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryCakeList[1],state = DISABLED)
txtCake1.grid(row=1,column =1)
txtCake2 = Entry(fCake,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryCakeList[2],state = DISABLED)
txtCake2.grid(row=2,column =1)
txtCake3 = Entry(fCake,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryCakeList[3],state = DISABLED)
txtCake3.grid(row=3,column =1)
txtCake4 = Entry(fCake,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryCakeList[4],state = DISABLED)
txtCake4.grid(row=4,column =1)
txtCake5 = Entry(fCake,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryCakeList[5],state = DISABLED)
txtCake5.grid(row=5,column =1)
txtCake6 = Entry(fCake,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryCakeList[6],state = DISABLED)
txtCake6.grid(row=6,column =1)
txtCake7 = Entry(fCake,font=('Adobe Hebrew',18,'bold'),bd=8,width=6,justify='left',textvariable=EntryCakeList[7],state = DISABLED)
txtCake7.grid(row=7,column =1)
#================================== Receipt Information ===================
_ = Label(fReceipt,font=('Adobe Hebrew',12,'bold'), text="Receipt", bd=2,anchor='w')
_.grid(row=0,column=0, sticky=W)
txtReceipt = Text(fReceipt,font=('Adobe Hebrew',11,'bold'), bd=8,width=59,height=22,bg="white")
txtReceipt.grid(row=1,column=0)
#=================================== Cost Items Information============
_ = Label(fCost1,font=('Adobe Hebrew',18,'bold'),text="Cost of Drinks",bd=8)
_.grid(row=0,column=0,sticky=W)
_=Entry(fCost1,font=('Adobe Hebrew',18,'bold'),bd=8,justify='left',
                      textvariable=CostofDrinks)
_.grid(row=0,column=1,sticky=W)

_ = Label(fCost1,font=('Adobe Hebrew',18,'bold'),text="Cost of Cakes",bd=8)
_.grid(row=1,column=0,sticky=W)
_=Entry(fCost1,font=('Adobe Hebrew',18,'bold'),bd=8,justify='left',
                     textvariable=CostofCakes)
_.grid(row=1,column=1,sticky=W)

_ = Label(fCost1,font=('Adobe Hebrew',18,'bold'),text="Service Charge",bd=8)
_.grid(row=2,column=0,sticky=W)
_=Entry(fCost1,font=('Adobe Hebrew',18,'bold'),bd=8,justify='left',
                       textvariable=ServiceCharge)
_.grid(row=2,column=1,sticky=W)

#=========================== Payment Information========================
_ = Label(fCost2,font=('Adobe Hebrew',18,'bold'),text="Paid Tax",bd=8)
_.grid(row=0,column=0,sticky=W)
_=Entry(fCost2,font=('Adobe Hebrew',18,'bold'),bd=8,justify='left',
                 textvariable=PaidTax)
_.grid(row=0,column=1,sticky=W)

_ = Label(fCost2,font=('Adobe Hebrew',18,'bold'),text="Sub Total",bd=8)
_.grid(row=1,column=0,sticky=W)
_=Entry(fCost2,font=('Adobe Hebrew',18,'bold'),bd=8,justify='left',
                  textvariable=SubTotal)
_.grid(row=1,column=1,sticky=W)

_ = Label(fCost2,font=('Adobe Hebrew',18,'bold'),text="Total",bd=8)
_.grid(row=2,column=0,sticky=W)
_=Entry(fCost2,font=('Adobe Hebrew',18,'bold'),bd=8,justify='left',
                   textvariable=TotalCost)
_.grid(row=2,column=1,sticky=W)
#================================== Button =========================
_=Button(fButton,padx=16, fg="black",font=('Adobe Hebrew',18,'bold'),width=5,
                text="Total",command=CostofItem).grid(row=0, column=0)
_=Button(fButton,padx=16, fg="black",font=('Adobe Hebrew',18,'bold'),width=5,
                text="Receipt",command=Receipt).grid(row=0, column=1)
_=Button(fButton,padx=16, fg="black",font=('Adobe Hebrew',18,'bold'),width=5,
                text="Reset",command=Reset).grid(row=0, column=2)
_=Button(fButton,padx=16, fg="black",font=('Adobe Hebrew',18,'bold'),width=5,
                text="Exit",command=qExit).grid(row=0, column=3)
_=Button(fButton2,padx=16, fg="black",font=('Adobe Hebrew',16,'bold'),width=20,
                text="Pay with credit card",command=Paywithcard).grid(row=1, column=0)




root.mainloop()
