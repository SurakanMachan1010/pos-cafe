from tkinter import*
import random
import time
import json
from PIL import Image,ImageTk
import smtplib
from email.mime.text import MIMEText
from ftplib import FTP
import datetime
import os
from tkinter import messagebox
import sys

if len(sys.argv) > 1:
    
    waitUID = sys.argv[1]
    print(f"Received UID: {waitUID}")
else:
    print("No UID provided.")
    

    
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

# ฟังก์ชันสำหรับกำหนดตำแหน่งหน้าต่างให้อยู่กลางจอ
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

# ฟังก์ชันสำหรับแสดงหน้าต่างตามหมายเลขหน้า
def ShowPage(page_number):
    global current_page
    current_page = page_number
    if page_number == 1:
        page1.pack(side=TOP)
        FLpage1.pack(side=TOP)
        
        page2.pack_forget()
        FLpage2.pack_forget()
        
        page3.pack_forget()
        FLpage3.pack_forget()
        
        page4.pack_forget()
        FLpage4.pack_forget()
        
        page5.pack_forget()
        FLpage5.pack_forget()
        
    elif page_number == 2:
        page1.pack_forget()
        FLpage1.pack_forget()
        
        page2.pack(side=TOP)
        FLpage2.pack(side=TOP)
        
        page3.pack_forget()
        FLpage3.pack_forget()
        
        page4.pack_forget()
        FLpage4.pack_forget()
        
        page5.pack_forget()
        FLpage5.pack_forget()
        
    elif page_number == 3:
        page1.pack_forget()
        FLpage1.pack_forget()
        
        page2.pack_forget()
        FLpage2.pack_forget()
        
        page3.pack(side=TOP)
        FLpage3.pack(side=TOP)
        
        page4.pack_forget()
        FLpage4.pack_forget()
        
        page5.pack_forget()
        FLpage5.pack_forget()
    
    elif page_number == 4:
        page1.pack_forget()
        FLpage1.pack_forget()
        
        page2.pack_forget()
        FLpage2.pack_forget()
        
        page3.pack_forget()
        FLpage3.pack_forget()
        
        page4.pack(side=TOP)
        FLpage4.pack(side=TOP)
        
        page5.pack_forget()
        FLpage5.pack_forget()
        
    elif page_number == 5:
        page1.pack_forget()
        FLpage1.pack_forget()
        
        page2.pack_forget()
        FLpage2.pack_forget()
        
        page3.pack_forget()
        FLpage3.pack_forget()
        
        page4.pack_forget()
        FLpage4.pack_forget()
        
        page5.pack(side=TOP)
        FLpage5.pack(side=TOP)

# ฟังก์ชันสำหรับเปลี่ยนไปหน้าถัดไป
def NextPage():
    new_page = current_page + 1
    if new_page <= total_pages:
        ShowPage(new_page)

# ฟังก์ชันสำหรับเปลี่ยนกลับไปหน้าก่อนหน้า
def PreviousPage():
    new_page = current_page - 1
    if new_page >= 1:
        ShowPage(new_page)

def PreviousPage2():
    ShowPage(2)

def Home():
    entry_uid.delete(0, END)
    ShowPage(1)

root = Tk()
root.title("ร้านค้าสวัสดิการ")

window_width = 800
window_height = 600

center_window(root, window_width, window_height)

# กำหนดจำนวนหน้าทั้งหมด
total_pages = 5
current_page = 1

# สร้างหน้าต่าง
page1 = Frame(root, width=800, height=600, relief=SUNKEN)
FLpage1 = Frame(root, width=200, height=30, relief=SUNKEN)

page2 = Frame(root, width=800, height=600, relief=SUNKEN)
FLpage2 = Frame(root, width=200, height=30, relief=SUNKEN)

page3 = Frame(root, width=800, height=600, relief=SUNKEN)
FLpage3 = Frame(root, width=200, height=30, relief=SUNKEN)

page4 = Frame(root, width=800, height=600, relief=SUNKEN)
FLpage4 = Frame(root, width=200, height=30, relief=SUNKEN)

page5 = Frame(root, width=800, height=600, relief=SUNKEN)
FLpage5 = Frame(root, width=200, height=30, relief=SUNKEN)

# ########################### funcทั้งหมด ###########################

# รูปไอคอน
icon_path = "resized_refresh_icon.png"
icon = Image.open(icon_path)
icon_resized1 = icon.resize((20, 20))
icon_resized2 = icon.resize((50, 50))
tk_image = ImageTk.PhotoImage(icon_resized1)
tk_image2 = ImageTk.PhotoImage(icon_resized2)
# ########################### page1 ###########################

def get_user_points(uid):   
    with open("card_data.json", "r") as file:
        data = json.load(file)
        for user in data:
            if user["uid"] == uid:
                return user["fullname"], user["points"], user["student_id"]
    return None, None  # หากไม่พบ UID ในไฟล์ JSON

def Next():
    uid = entry_uid.get()
    # send_email(uid)

    ShowPage(2)

    # เรียกใช้ฟังก์ชัน get_user_points เพื่อดึงข้อมูลผู้ใช้
    fullname, points, student_id = get_user_points(uid)
    if fullname is not None and points is not None:
        # แสดงข้อมูลในหน้า 2
        Label(page2, font=('TH Saraban New', 10, 'bold'),
              text="ID : {}".format(student_id), fg="bisque3", bd=10, anchor='w', pady=1).grid(row=2, column=0)
        Label(page2, font=('TH Saraban New', 10, 'bold'),
              text="Username : {}".format(fullname), fg="bisque3", bd=10, anchor='w', pady=1).grid(row=3, column=0)
        Label(page2, font=('TH Saraban New', 10, 'bold'),
              text="Point : {}".format(points), fg="bisque3", bd=10, anchor='w', pady=1).grid(row=4, column=0)
    else:
        # หากไม่พบข้อมูล UID ให้แสดงข้อความที่แสดงว่าไม่พบข้อมูล
        list_label.config(text="ไม่พบข้อมูลสำหรับ UID: {uid}".format(uid=uid))


# ########################### page2 ###########################
def CalTotal():
    global CostofMeal
    x = random.randint(12908, 508764)
    rand.set(str(x))
    
    def get_menu_value(menu_entry):
        try:
            value = int(menu_entry.get())
        except:
            menu_entry.set(0)
            value = 0
        return value
    
    CoMenu1 = get_menu_value(Menu1)
    CoMenu2 = get_menu_value(Menu2)
    CoMenu3 = get_menu_value(Menu3)
    CoMenu4 = get_menu_value(Menu4)
    CoMenu5 = get_menu_value(Menu5)
    CoMenu6 = get_menu_value(Menu6)
    CoMenu7 = get_menu_value(Menu7)
    
    CoMenu1 *= MenuPrice[0]
    CoMenu2 *= MenuPrice[1]
    CoMenu3 *= MenuPrice[2]
    CoMenu4 *= MenuPrice[3]
    CoMenu5 *= MenuPrice[4]
    CoMenu6 *= MenuPrice[5]
    CoMenu7 *= MenuPrice[6]
    
    CostofMeal = CoMenu1 + CoMenu2 + CoMenu3 + CoMenu4 + CoMenu5 + CoMenu6 + CoMenu7
    CostofMealB = "%.0f P" % CostofMeal
    Cost.set(CostofMealB)
                            
def Reset():
    rand.set("")
    Menu1.set("")
    Menu2.set("")
    Menu3.set("")
    Menu4.set("")
    Menu5.set("")
    Menu6.set("")
    Menu7.set("")
    Cost.set("")
    # Total.set("")
    # Tax.set("")
    # TotalTax.set("")
    
rand = StringVar()

#ข้อมูล
rand = StringVar()
Cost = StringVar()
Menu1 = StringVar()
Menu2 = StringVar()
Menu3 = StringVar()
Menu4 = StringVar()
Menu5 = StringVar()
Menu6 = StringVar()
Menu7 = StringVar()

MenuPrice = [10, 20, 25, 30, 40, 100, 500]

text_Input = StringVar()
operator = ""


# ########################### page3 ###########################
def ExitP():
    root.quit()

def refreshClicked():
    # ล้างข้อมูลในกล่องข้อความ
    entry_otp.delete(0, END)
    print("ส่งรหัส OTP ใหม่")

    # เรียกใช้ฟังก์ชัน send_email_to_user เพื่อส่งรหัส OTP ใหม่
    uid = entry_uid.get()
    if uid:
        send_email(uid)

    # ลบ Label ที่แสดงข้อความ "OTP ไม่ถูกต้อง" ออกจาก GUI
    for widget in FLpage3.winfo_children():
        if isinstance(widget, Label) and widget.cget("text") == "OTP ไม่ถูกต้อง":
            widget.destroy()


def generate_random_code():
    return ''.join(random.choices('0123456789', k=6))

def read_user_data(uid):
    
    with open("card_data.json", "r") as file:  # เปลี่ยนจาก "user.json" เป็น "card_data.json"
        data = json.load(file)
        for user in data:
            if user["uid"] == uid:
                return user["email"]
    return None

def send_email_to_user(username_with_kuth):
    random_code = generate_random_code()
    msg = MIMEText("รหัสยืนยันของคุณคือ: {}".format(random_code))
    msg['Subject'] = 'รหัสยืนยัน'
    msg['From'] = 'supakorn.di@ku.th'  
    msg['To'] = username_with_kuth

    smtp_server = 'smtp.gmail.com'  

    try:
        smtp_conn = smtplib.SMTP(smtp_server, 587)
        smtp_conn.ehlo()
        smtp_conn.starttls()
        smtp_conn.login('supakorn.di@ku.th', '0845481577@Jim')  
        smtp_conn.send_message(msg)
        smtp_conn.quit()
        return random_code

    except Exception as e:
        print("เกิดข้อผิดพลาดในการส่งอีเมล:", e)

def send_email(uid):
    email = read_user_data(uid)
    if email:
        random_code = send_email_to_user(email)
        if random_code:
            print("ส่ง OTP ไปยังอีเมล {} สำเร็จ".format(email))
            # button_send_uid.grid_remove()  
            # entry_uid.grid_remove()  
            
            # Remove the following line to fix the error
            # label_uid.grid_remove()  
            
            # entry_otp.grid(row=5, column=0, padx=5, pady=5)  
            # label_otp.grid(row=1, column=0, sticky="w")  
            button_send_otp.config(command=lambda: submit_otp(entry_otp.get(), random_code))


def check_otp(otp, random_code):
    if otp.isdigit() and otp == random_code:
        return True
    else:
        print("กรุณากรอก OTP ให้ถูกต้อง")
        return False

def submit_otp(otp, random_code):
    global CostofMeal
    if check_otp(otp, random_code):
        ShowPage(4)
        uid = entry_uid.get()  
        update_user_points(uid, CostofMeal)
    else:
        print("กรอก OTP ใหม่")  
        entry_otp.delete(0, END)  
        label_otp_error = Label(FLpage3, font=('TH Saraban New', 20, 'bold'),text="OTP ไม่ถูกต้อง",
                                fg="red", bd=10, anchor='w', pady=1)
        label_otp_error.grid(row=7, column=0, padx=10, pady=10)
        uid = entry_uid.get()
        if uid:
            user_email = read_user_data(uid)


def button_send_uid_clicked():
    uid = entry_uid.get()
    send_email(uid)

    ShowPage(3)

        
def OkClicked():
    pass

def NoClicked():
    pass


def SendOtpClicked():
    pass

def get_user_points(uid):
    with open("card_data.json", "r") as file:
        data = json.load(file)
        for user in data:
            if user["uid"] == uid:
                return user["fullname"], user["points"]
    return None, None  # หากไม่พบ UID ในไฟล์ JSON

def update_user_points(uid, used_points):
     # อ่านข้อมูลจากไฟล์ JSON
    with open("card_data.json", "r") as file:
        data = json.load(file)
    
    # ค้นหา UID ที่ตรงกับที่ผู้ใช้ป้อนเข้ามา
    for user in data:
        if user["uid"] == uid:
            # ลบจำนวนแต้มที่ใช้ไปออกจากยอดแต้มปัจจุบัน
            user["points"] -= used_points
    
    # บันทึกข้อมูลที่อัปเดตลงในไฟล์ JSON โดยจัดรูปแบบข้อมูลให้ดูสวยงาม
    with open("card_data.json", "w") as file:
        json.dump(data, file, indent=4)
    upload_file(ftp, filename)

    # เรียกใช้ฟังก์ชัน get_user_points เพื่อดึงข้อมูลผู้ใช้
    fullname, points = get_user_points(uid)
    if fullname is not None and points is not None:
        # แสดงข้อมูลในหน้า 4
        list_label.config(text="ชื่อ: {fullname}  แต้มคงเหลือ: {points}".format(fullname=fullname, points=points))
    else:
        list_label.config(text="ไม่พบข้อมูลสำหรับ UID: {uid}".format(uid=uid))


# ในฟังก์ชัน CalTotal() หลังจากที่คุณคำนวณจำนวนแต้มที่ใช้ไปแล้ว คุณสามารถเรียกใช้ฟังก์ชัน update_user_points() เพื่อลบจำนวนแต้มที่ใช้ไปออกจากยอดแต้มปัจจุบันของผู้ใช้ได้ เช่นนี้:



# สังเกตว่าฟังก์ชัน CalTotal() ถูกแก้ไขโดยการเรียกใช้ update_user_points() หลังจากที่คำนวณค่าทั้งหมดแล้ว

# ########################### page4 ###########################

# เมื่อคลิกปุ่มส่ง UID ให้เรียกใช้ฟังก์ชันนี้
def button_send_uid_clicked():
    uid = entry_uid.get()

    # เรียกใช้ฟังก์ชัน get_user_points เพื่อดึงข้อมูลผู้ใช้
    fullname, points = get_user_points(uid)
    
    if fullname is not None and points is not None:
        # เช็คว่า CostofMeal ไม่เท่ากับ 0 และจำนวนแต้มมีพอสำหรับการแลก
        if CostofMeal != 0 and points >= CostofMeal:
            # ลดจำนวนแต้มที่ใช้ไป
            send_email(uid)

            ShowPage(3)

            list_label.config(text="ชื่อ: {fullname}  แต้มคงเหลือ: {points}".format(fullname=fullname, points=points - CostofMeal))
        else:
            ShowPage(5)
    else:
        list_label.config(text="ไม่พบข้อมูลสำหรับ UID: {uid}".format(uid=uid))
        
def get_user_market(uid):
    with open("card_data.json", "r") as file:
        data = json.load(file)
        for user in data:
            if user["uid"] == uid:
                return user["student_id"],user["fullname"], user["points"]
    return None, None  # หากไม่พบ UID ในไฟล์ JSON

def market():
    uid = entry_uid.get()

    ShowPage(2)

    # เรียกใช้ฟังก์ชัน get_user_market เพื่อดึงข้อมูลผู้ใช้
    student_id,fullname, points = get_user_market(uid)
    if student_id is not None and fullname is not None and points is not None:
        # แสดงข้อมูลในหน้า 4
        uid_label_market.config(text="ID: {student_id}"
            .format(student_id=student_id))
        name_label_market.config(text="ชื่อ: {fullname}"
            .format(fullname=fullname))
        point_label_market.config(text="แต้ม: {points}"
            .format(points=points))
    else:
        list_label.config(text="ไม่พบข้อมูลสำหรับ UID: {uid}".format(uid=uid))

#----------------------------`เรียกข้อมูลหน้าแรก`------------------------------------------------
def get_user_info(uid):
    with open("card_data.json", "r") as file:
        data = json.load(file)
        for user in data:
            if user["uid"] == uid:
                return user["student_id"],user["fullname"], user["points"]
    return None, None  # หากไม่พบ UID ในไฟล์ JSON

def info_user():
    uid = entry_uid.get()

    ShowPage(1)

    # เรียกใช้ฟังก์ชัน get_user_market เพื่อดึงข้อมูลผู้ใช้
    student_id,fullname, points = get_user_info(uid)
    if student_id is not None and fullname is not None and points is not None:
        # แสดงข้อมูลในหน้า 4
        uid_label_info.config(text="ID: {student_id}"
            .format(student_id=student_id))
        name_label_info.config(text="ชื่อ: {fullname}"
            .format(fullname=fullname))
        point_label_info.config(text="แต้ม: {points}"
            .format(points=points))
    else:
        list_label.config(text="ไม่พบข้อมูลสำหรับ UID: {uid}".format(uid=uid))
        
        
# ########################### ข้อมูลในหน้าแรก ###########################
_ = Label(page1, font=('TH Saraban New', 50, 'bold'),
          text="แลกแต้ม", fg="bisque4", bd=10, anchor='w', pady=1)
_.grid(row=1, column=1)

_ = Label(page1, font=('TH Saraban New', 20, 'bold'),
          text="          ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿          ", fg="bisque3", bd=10, anchor='w', pady=1).grid(row=2, column=1)

# _ = Label(page1, font=('TH Saraban New', 40, 'bold'),
#           text="กรุณาแตะบัตร....", fg="bisque3", bd=10, anchor='w', pady=1, padx=2).grid(row=3, column=1)

uid_label_info = Label(page2, font=('TH Saraban New', 10, 'bold'), fg="bisque3", bd=10, anchor='w', pady=1)
uid_label_info.grid(row=2, column=0)
name_label_info = Label(page2, font=('TH Saraban New', 10, 'bold'), fg="bisque3", bd=10, anchor='w', pady=1)
name_label_info.grid(row=3, column=0)
point_label_info = Label(page2, font=('TH Saraban New', 10, 'bold'), fg="bisque3", bd=10, anchor='w', pady=1)
point_label_info.grid(row=4, column=0)
# 
entry_uid = Entry(FLpage1, font=('TH Sarabun New', 20))
entry_uid.insert(0, waitUID)
entry_uid.grid(row=3, column=0, padx=5, pady=5)
entry_uid.config(state='readonly')  # ตั้งค่า state เป็น 'readonly' เพื่อป้องกันการแก้ไขข้อมูล

label_otp=Label(FLpage1, font=('TH Saraban New', 30, 'bold'),
                fg="bisque4", bd=10, anchor='w', pady=1)

# ปุ่มไปหน้าแลกแต้ม
_ = Button(FLpage1,bd=8,fg='black',font=('TH Sarabun New',10,'bold'),
           text="next",bg="bisque1",command=market).grid(row=4,column=4)

# ########################### ข้อมูลในหน้าที่สอง ###########################

#Top
_ = Label(page2, font=('TH Saraban New', 50, 'bold'),
          text="แลกแต้ม", fg="bisque4", bd=10, anchor='w', pady=1)
_.grid(row=0, column=0)

_ = Label(page2, font=('TH Saraban New', 20, 'bold'),
          text="✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ", fg="bisque3", bd=10, anchor='w', pady=1).grid(row=1, column=0)

uid_label_market = Label(page2, font=('TH Saraban New', 10, 'bold'), fg="bisque3", bd=10, anchor='w', pady=1)
uid_label_market.grid(row=2, column=0)
name_label_market = Label(page2, font=('TH Saraban New', 10, 'bold'), fg="bisque3", bd=10, anchor='w', pady=1)
name_label_market.grid(row=3, column=0)
point_label_market = Label(page2, font=('TH Saraban New', 10, 'bold'), fg="bisque3", bd=10, anchor='w', pady=1)
point_label_market.grid(row=4, column=0)

#ซ้าย
#1
_ = Label(FLpage2, font=('TH Saraban New', 12, 'bold'),
          text="แก้วน้ำ 10P", fg="bisque4", bd=16, anchor='w').grid(row=0, column=0)
_ = Entry(FLpage2, font=('TH Sarabun New', 12,'bold'),
          textvariable=Menu1,bd=10,insertwidth=4,bg="bisque3",
          justify="right").grid(row=0, column=1)
#2
_ = Label(FLpage2, font=('TH Saraban New', 12, 'bold'),
          text="ผ้าห่ม 20P", fg="bisque4", bd=16, anchor='w').grid(row=1, column=0)
_ = Entry(FLpage2, font=('TH Sarabun New', 12,'bold'),
          textvariable=Menu2,bd=10,insertwidth=4,bg="bisque3",
          justify="right").grid(row=1, column=1)
#3
_ = Label(FLpage2, font=('TH Saraban New', 12, 'bold'),
          text="กระเป๋า 25P", fg="bisque4", bd=16, anchor='w').grid(row=2, column=0)
_ = Entry(FLpage2, font=('TH Sarabun New', 12,'bold'),
          textvariable=Menu3,bd=10,insertwidth=4,bg="bisque3",
          justify="right").grid(row=2, column=1)
#4
_ = Label(FLpage2, font=('TH Saraban New', 12, 'bold'),
          text="โต๊ะพับ 30P", fg="bisque4", bd=16, anchor='w').grid(row=3, column=0)
_ = Entry(FLpage2, font=('TH Sarabun New', 12,'bold'),
          textvariable=Menu4,bd=10,insertwidth=4,bg="bisque3",
          justify="right").grid(row=3, column=1)
#5
_ = Label(FLpage2, font=('TH Saraban New', 12, 'bold'),
          text="พัดลม 40P", fg="bisque4", bd=16, anchor='w').grid(row=4, column=0)
_ = Entry(FLpage2, font=('TH Sarabun New', 12,'bold'),
          textvariable=Menu5,bd=10,insertwidth=4,bg="bisque3",
          justify="right").grid(row=4, column=1)
#6
_ = Label(FLpage2, font=('TH Saraban New', 12, 'bold'),
          text="จักรยาน 100P", fg="bisque4", bd=16, anchor='w').grid(row=0, column=2)
_ = Entry(FLpage2, font=('TH Sarabun New', 12,'bold'),
          textvariable=Menu6,bd=10,insertwidth=4,bg="bisque3",
          justify="right").grid(row=0, column=3)
#7
_ = Label(FLpage2, font=('TH Saraban New', 12, 'bold'),
          text="ทีวีจอแบน 500P", fg="bisque4", bd=16, anchor='w').grid(row=1, column=2)
_ = Entry(FLpage2, font=('TH Sarabun New', 12,'bold'),
          textvariable=Menu7,bd=10,insertwidth=4,bg="bisque3",
          justify="right").grid(row=1, column=3)

#----------------------------------------------------------------------------------------------------ช่องเก็บจำนวนแต้ม
_ = Label(FLpage2, font=('TH Saraban New', 15, 'bold'),
          text="จำนวนแต้มที่ใช้ :", fg="bisque4", bd=16, anchor='w').grid(row=3, column=2)
totalP= Entry(FLpage2, font=('TH Sarabun New', 15,'bold'),
          textvariable=Cost,insertwidth=4,bg="white",
          justify="right")
totalP.grid(row=3, column=3)
totalP.config(state='readonly')

_ = Button(FLpage2,bd=8,width=55,fg='black',font=('TH Sarabun New', 18,'bold'),
           image=tk_image ,bg="bisque1",command=Reset).grid(row=4,column=2,padx=2)
#Btn Total
_ = Button(FLpage2,bd=8,width=10,fg='black',font=('TH Sarabun New',10,'bold'),
           text="Total",bg="bisque1",command=CalTotal).grid(row=4,column=3,padx=2)

# ปุ่มแลกแต้ม(ส่งOTP)
button_send_uid = Button(FLpage2,bd=8,width=10,fg='black',font=('TH Sarabun New',10,'bold'),
           text="แลก",bg="bisque1", command=button_send_uid_clicked).grid(row=5,column=2,padx=2)

_ = Button(FLpage2,bd=8,width=10,fg='black',font=('TH Sarabun New',10,'bold'),
           text="Exit",bg="bisque1",command=ExitP).grid(row=5,column=3)

# _ = Button(FLpage2,bd=8,fg='black',font=('TH Sarabun New',10,'bold'),
#            text="แลก",bg="bisque1",command=NextPage).grid(row=4,column=4)

# ########################### ข้อมูลในหน้าที่สาม ###########################

#Top
_ = Label(page3, font=('TH Saraban New', 50, 'bold'),
          text="รหัส OTP", fg="bisque4", bd=10, anchor='w', pady=1)
_.pack()

_ = Label(page3, font=('TH Saraban New', 20, 'bold'),
          text="✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ", fg="bisque3", bd=10, anchor='w', pady=1)
_.pack()

entry_otp = Entry(FLpage3, font=('TH Sarabun New', 20))
entry_otp.grid(row=5, column=1, padx=5, pady=50)

# ปุ่ม refresh
refresh_button = Button(FLpage3, padx=20, bd=8, pady=2, fg='black', bg="bisque1", 
                        image=tk_image2, command=refreshClicked)
refresh_button.grid(row=6, column=0, padx=70, pady=20)

# ปุ่มยืนยัน
button_send_otp = Button(FLpage3, padx=20, bd=8, pady=2, fg='black', 
                         font=('TH Sarabun New', 20, 'bold'),
                         text="ยืนยัน", bg="bisque1", command=SendOtpClicked)
button_send_otp.grid(row=6, column=2, padx=80, pady=30)


# _ = Button(FLpage3,bd=8,fg='black',font=('TH Sarabun New',10,'bold'),
#            text="Back",bg="bisque1",command=PreviousPage).grid(row=4,column=3)
# _ = Button(FLpage3,bd=8,fg='black',font=('TH Sarabun New',10,'bold'),
#            text="next",bg="bisque1",command=NextPage).grid(row=4,column=4)




# ########################### ข้อมูลในหน้าที่สี่ ###########################
#Top
_ = Label(page4, font=('TH Saraban New', 80, 'bold'),
          text="แลกแต้มสำเร็จ", fg="bisque4", bd=10, anchor='w', pady=1)
_.pack()

_ = Label(page4, font=('TH Saraban New', 20, 'bold'),
          text="✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ", fg="bisque3", bd=10, anchor='w', pady=1)
_.pack()
list_label = Label(FLpage4, font=('TH Saraban New', 20, 'bold'),fg="bisque3")
list_label.grid(row=2, column=0, padx=20, pady=50)


# ปุ่มออก
_ = Button(FLpage4,bd=8,width=20,fg='black',font=('TH Sarabun New',10,'bold'),
           text="Exit",bg="bisque1",command=ExitP).grid(row=4,column=0)


# ########################### ข้อมูลในหน้าที่ห้า(ยังไม่ใช้) ###########################

_ = Label(page5, font=('TH Saraban New', 100, 'bold'),
          text="error", fg="bisque4", bd=10, anchor='w', pady=1)
_.pack()

_ = Label(page5, font=('TH Saraban New', 20, 'bold'),
          text="✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ", fg="bisque3", bd=10, anchor='w', pady=1)
_.pack()
_ = Label(page5, font=('TH Saraban New', 15, 'bold'),
          text="แลกแต้มไม่สำเร็จ กรุณาลองใหม่", fg="red", bd=10, anchor='w', pady=1)
_.pack()

_ = Button(FLpage5,bd=8,fg='black',font=('TH Sarabun New',10,'bold'),
           text="Back",bg="bisque1",command=PreviousPage2).grid(row=4,column=3)


# ////////////////////////////////////////////////////////////////////

# แสดงหน้าแรกเมื่อเริ่มต้นโปรแกรม
ShowPage(1)

root.mainloop()

