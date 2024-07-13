import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.scard import (
    SCardEstablishContext, SCardListReaders, SCardConnect, SCardTransmit,
    SCardGetErrorMessage, SCARD_S_SUCCESS, SCARD_SCOPE_USER,
    SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0, SCARD_PROTOCOL_T1
)
import json
import subprocess
import threading
from ftplib import FTP
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

ip = '10.64.194.31'
user = 'NetPro'
passwd = '123456'
filename = 'card_data.json'

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue") 

ftp = connect_ftp_server(ip, user, passwd)
download_file(ftp, filename)

cardId = None
message_label = None

def load_json_data(file_path):
    with open(file_path, encoding='utf-8') as file:
        return json.load(file)

def get_card_uid():
    try:
        hresult, context = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult != SCARD_S_SUCCESS:
            print("Failed to establish context:", SCardGetErrorMessage(hresult))
            return None
        hresult, readers = SCardListReaders(context, [])
        if hresult != SCARD_S_SUCCESS:
            print("Failed to list readers:", SCardGetErrorMessage(hresult))
            return None
        if readers:
            reader = readers[0]
            hresult, hcard, dwActiveProtocol = SCardConnect(context, reader, SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
            if hresult != SCARD_S_SUCCESS:
                print("Failed to connect to the card:", SCardGetErrorMessage(hresult))
                return None
            command = [0xFF, 0xCA, 0x00, 0x00, 0x04]
            hresult, response = SCardTransmit(hcard, dwActiveProtocol, command)
            if hresult == SCARD_S_SUCCESS:
                uid = ''.join(['%02X' % b for b in response[:-2]])
                return uid
            else:
                print("Failed to retrieve card UID:", SCardGetErrorMessage(hresult))
        else:
            print("No smart card readers found")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


class NFCReaderThread(threading.Thread, CardObserver):
    def __init__(self, update_ui_callback):
        threading.Thread.__init__(self)
        CardObserver.__init__(self)
        self.cardMonitor = CardMonitor()
        self.cardMonitor.addObserver(self)
        self.update_ui_callback = update_ui_callback
        self.daemon = True

    def update(self, observable, actions):
        global cardId
        (addedcards, removedcards) = actions
        for card in addedcards:
            cardId = get_card_uid()
            self.update_ui_callback(cardId)  # Call the update UI callback

    def run(self):
        while True:
            pass

def display_user_info(root, frame):
    global cardId, message_label
    if cardId:
        data = load_json_data(filename)
        found = False
        for user in data:
            if user["uid"] == cardId:
                student_id = user.get('student_id', 'N/A')
                name = user.get('fullname', 'N/A')
                balance = user.get('balance', 'N/A')
                display_str = f"Student ID: {student_id}, Name: {name}, Balance: {balance}"
                if message_label:
                    message_label.destroy()
                message_label = ttk.Label(frame, text=display_str, background='#E0FFFF', foreground='#000080', font=('Arial', 10, 'bold'))
                message_label.pack(pady=5, padx=10, fill='x')
                found = True
                break
        if not found and message_label is None:
            messagebox.showwarning("ไม่พบข้อมูล", "ไม่พบข้อมูลสำหรับ UID นี้ในระบบ")
    else:
        if message_label is None:
            message_label = ttk.Label(frame, text="Please scan your card...", background='#E0FFFF', foreground='#000080', font=('Arial', 10, 'bold'))
            message_label.pack(pady=5, padx=10, fill='x')

def ExitP():
    delete_file(filename)
    ftp.quit()
    

def create_purchase_window1():
    subprocess.run(["python", "Cafe1.py"], check=True)

def create_purchase_window2():
    subprocess.run(["python", "Cafe2.py"], check=True)

def create_main_window():
    ctk.set_appearance_mode("Dark")  
    ctk.set_default_color_theme("blue") 

    root = tk.Tk()
    root.title("User Information")
    root.geometry("1000x600")
    root.configure(background='#E0FFFF')

    main_frame = ctk.CTkFrame(root, corner_radius=10)
    main_frame.pack(pady=20, padx=20, fill='both', expand=True)

    center_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    center_frame.pack(pady=20, padx=20, fill='both', expand=True)

    update_ui = lambda cardId: display_user_info(root, center_frame)
    nfc_thread = NFCReaderThread(update_ui)
    nfc_thread.start()

    # This frame now packs at the bottom of the main_frame
    buttons_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    buttons_frame.pack(side='bottom', pady=10, padx=10, fill='x', expand=False)

    # Configure buttons_frame for grid placement
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid_columnconfigure(1, weight=1)
    buttons_frame.grid_columnconfigure(2, weight=1)

    purchase_button1 = ctk.CTkButton(buttons_frame, text="Coffee Cafe", command=lambda: create_purchase_window1())
    purchase_button1.grid(row=0, column=0, padx=10, pady=10, sticky='W')

    exit_button = ctk.CTkButton(buttons_frame, text="Exit", command=lambda: [ExitP(), root.destroy()])
    exit_button.grid(row=0, column=1, padx=10, pady=10)  # Centered by placing in the middle column

    purchase_button2 = ctk.CTkButton(buttons_frame, text="Cafe Shop", command=lambda: create_purchase_window2())
    purchase_button2.grid(row=0, column=2, padx=10, pady=10, sticky='E')

    return root


if __name__ == "__main__":
    app = create_main_window()
    #nfc_thread = NFCReaderThread()
    #nfc_thread.start()
    app.mainloop()