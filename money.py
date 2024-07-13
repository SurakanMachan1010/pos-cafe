import customtkinter as ctk
import tkinter as tk
import json
from ftplib import FTP
from typing import List
from tkinter import messagebox
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.scard import (
    SCardEstablishContext, SCardListReaders, SCardConnect, SCardTransmit,
    SCardGetErrorMessage, SCardStatus, SCARD_S_SUCCESS, SCARD_SCOPE_USER,
    SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0, SCARD_PROTOCOL_T1
)
import datetime
import os
from subprocess import call

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

ctk.set_appearance_mode("Dark")  # เลือกโหมดการแสดงผล "Dark" หรือ "Light"
ctk.set_default_color_theme("blue")  # เลือกธีมสี (มีหลายตัวเลือก เช่น "blue", "green", "dark-blue")

class NFCObserver(CardObserver):
    download_file(ftp, filename)
    def __init__(self, data_file, registration_window):
        super().__init__()
        self.data_file = data_file
        self.registration_window = registration_window
        self.load_data()
        self.uid = None

    def get_card_uid(self):
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

    def update(self, observable, actions):
        (addedcards, _) = actions

        for card in addedcards:
            # Fetch the UID using the new method
            self.uid = self.get_card_uid()
            
            if self.uid is None:
                print("Could not read card UID")
                continue  # Skip further processing if UID couldn't be read

            # Check if the UID is in the data list
            if any(uid_dict['uid'] == self.uid for uid_dict in self.data):
                self.display_card_data(self.uid)
            else:
                messagebox.showinfo("Card Not Registered", f"Card with UID {self.uid} is not registered. Please register.")
                self.registration_window.lift()
                # Reset all fields when card is not registered
                self.reset_fields()

    def reset_fields(self):
        # Reset all entry fields to empty strings
        self.registration_window.entry_student_id.delete(0, tk.END)
        self.registration_window.entry_email.delete(0, tk.END)
        self.registration_window.entry_name.delete(0, tk.END)
        self.registration_window.entry_full_name.delete(0, tk.END)
        self.registration_window.entry_points.delete(0, tk.END)


    def display_card_data(self, uid):
        # Retrieve data based on UID from dictionary
        student_data = self.data[uid]

        # Display data in entry fields
        self.registration_window.entry_student_id.delete(0, tk.END)
        self.registration_window.entry_student_id.insert(0, student_data["student_id"])

        self.registration_window.entry_email.delete(0, tk.END)
        self.registration_window.entry_email.insert(0, student_data["email"])

        self.registration_window.entry_points.delete(0, tk.END)
        self.registration_window.entry_points.insert(0, student_data.get("points", 0))  # Display points, default to 0 if not present

        # Check if there is enough data in "fullname"
        if "fullname" in student_data:
            fullname_parts = student_data["fullname"].split()
            if len(fullname_parts) >= 2:
                self.registration_window.entry_name.delete(0, tk.END)
                self.registration_window.entry_name.insert(0, fullname_parts[0])

                self.registration_window.entry_full_name.delete(0, tk.END)
                self.registration_window.entry_full_name.insert(0, fullname_parts[1])
            else:
                messagebox.showerror("Error", "Invalid 'fullname' data in the dictionary.")
        else:
            messagebox.showerror("Error", "No 'fullname' data found in the dictionary.")

        # Display top-up history if available
        if 'history' in student_data:
            history = student_data['history']
            history_str = "\n".join([f"Amount: {record['amount']}, Date: {record['datetime']}" for record in history])
            messagebox.showinfo("Top-up History", history_str)



    def register_card_data(self, name, uid, student_id, email, full_name, points):
        # Check if UID already exists in the data list
        if any(uid_dict['uid'] == uid for uid_dict in self.data):
            messagebox.showerror("Error", f"Card with UID {uid} is already registered.")
        else:
            # Append new data to the data list
            self.data.append({'uid': uid, 'balance': 0, 'student_id': student_id, 'email': email, 'fullname': name+" "+full_name, 'points': points})
            self.save_data()
            messagebox.showinfo("Success", "Card registration successful.")

    def top_up_balance(self, uid):
        if uid in [item['uid'] for item in self.data]:
            self.amount_window = tk.Toplevel()
            self.amount_window.title("Enter Amount")

            label_amount = tk.Label(self.amount_window, text="Enter the amount to top up:", font=("Helvetica", 12))
            label_amount.pack(padx=10, pady=10)

            entry_amount = tk.Entry(self.amount_window, font=("Helvetica", 12))
            entry_amount.pack(padx=10, pady=10)

            def get_amount():
                try:
                    amount = float(entry_amount.get())
                    self.amount_window.destroy()
                    self.amount_window = None
                    self.process_top_up(uid, amount)
                    # Update top-up history
                    self.update_top_up_history(uid, amount)
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

            button_submit = tk.Button(self.amount_window, text="Submit", command=get_amount, font=("Helvetica", 12), bg="green", fg="white")
            button_submit.pack(padx=10, pady=10)
        else:
            messagebox.showerror("Error", f"Card with UID {uid} is not registered.")


    def process_top_up(self, uid, amount):
        if amount is not None:
            for item in self.data:
                if item['uid'] == uid:
                    item['balance'] += amount
                    break
            else:
                self.data.append({'uid': uid, 'balance': amount})
            
            self.save_data()
            messagebox.showinfo("Success", f"Top-up successful for card with UID: {uid}, Amount: {amount}")


    def update_top_up_history(self, uid, amount):
        for item in self.data:
            if item['uid'] == uid:
                if 'history' not in item:
                    item['history'] = []  # สร้างรายการประวัติการเติมเงินถ้ายังไม่มี
                item['history'].append({'amount': amount, 'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'type': 'topup', 'service': 'office'})
                break  # หลังจากพบ UID ที่ตรงกันแล้วให้หยุดวนลูป
        self.save_data()


    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
                if not isinstance(self.data, list):
                    self.data = [self.data]  # แปลงให้เป็นลิสต์หากไม่ใช่
        except FileNotFoundError:
            self.data = []


    def save_data(self):
        data_with_uid = [{'uid': item['uid'], **item} for item in self.data]
        with open(self.data_file, 'w') as file:
            json.dump(data_with_uid, file, indent=4)
        upload_file(ftp, filename)

    def get_uid(self):
        return self.uid

class NFCRegistrationWindow(ctk.CTk):
    def __init__(self, data_file):
        super().__init__()
        self.title("Card Top-up System")
        self.geometry("400x875")
        self.data_file = data_file
        self.nfc_observer = NFCObserver(data_file, self)

        # Start Reading Button
        self.button_start_reading = ctk.CTkButton(self, text="Start Reading", command=self.start_reading)
        self.button_start_reading.pack(pady=10)
        self.bind("<Return>", self.start_reading)

        # Top Up Balance Button
        self.button_top_up = ctk.CTkButton(self, text="Top Up Balance", command=self.top_up_balance)
        self.button_top_up.pack(pady=10)

        # View Top-up History Button
        self.button_top_up_history = ctk.CTkButton(self, text="View History", command=self.view_top_up_history)
        self.button_top_up_history.pack(pady=10)

        # UID Entry
        self.label_uid = ctk.CTkLabel(self, text="Enter the UID of your card:")
        self.label_uid.pack(pady=10)
        self.entry_uid = ctk.CTkEntry(self)
        self.entry_uid.pack(pady=10)

        # Student ID Entry
        self.label_student_id = ctk.CTkLabel(self, text="Enter your student ID:")
        self.label_student_id.pack(pady=10)
        self.entry_student_id = ctk.CTkEntry(self)
        self.entry_student_id.pack(pady=10)

        # Email Entry
        self.label_email = ctk.CTkLabel(self, text="Enter your email:")
        self.label_email.pack(pady=10)
        self.entry_email = ctk.CTkEntry(self)
        self.entry_email.pack(pady=10)

        # Name Entry
        self.label_name = ctk.CTkLabel(self, text="Enter your first name:")
        self.label_name.pack(pady=10)
        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.pack(pady=10)

        # Full Name Entry
        self.label_full_name = ctk.CTkLabel(self, text="Enter your last name:")
        self.label_full_name.pack(pady=10)
        self.entry_full_name = ctk.CTkEntry(self)
        self.entry_full_name.pack(pady=10)

        # Points Entry
        self.label_points = ctk.CTkLabel(self, text="Enter your accumulated points:")
        self.label_points.pack(pady=10)
        self.entry_points = ctk.CTkEntry(self)
        self.entry_points.pack(pady=10)
        self.entry_points.insert(0, "0")  # Default points value to 0

        # Register Card Button
        self.button_register = ctk.CTkButton(self, text="Register Card", command=self.register_card)
        self.button_register.pack(pady=10)
        
        self.button_register = ctk.CTkButton(self, text="Redeem Points", command=self.redeem_points)
        self.button_register.pack(pady=10)

        self.button_exit = ctk.CTkButton(self, text="Exit", command=self.exit_program)
        self.button_exit.pack(pady=10)

        self.update_default_uid()

    def exit_program(self):
        delete_file(filename)
        ftp.quit()
        self.destroy()
        return

    def redeem_points(self):
        delete_file(filename)
        ftp.quit()
        # รับค่า UID
        uid = self.entry_uid.get()
        
        # เรียกใช้ main.py พร้อมกับส่งค่า UID
        call(['python', 'main.py', uid])
        
    def view_top_up_history(self):
        uid = self.entry_uid.get()
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    history_str = ""
                    for item in data:
                        if item.get('uid') == uid and 'history' in item:
                            # Iterate through each record in the history
                            for record in item['history']:
                                if record['type'] == 'topup':
                                    history_str += f"+ Topup Amount: {record['amount']}, Date: {record['datetime']}\n"
                                elif record['type'] == 'pay':
                                    history_str += f"- Pay at {record['service']} Amount: {record['amount']}, Point: {record['point']}, Date: {record['datetime']}\n"
                    
                    if history_str:  # If history_str is not empty, show the history
                        messagebox.showinfo("History", history_str.rstrip())  # Use rstrip() to remove the last newline
                        return
                    else:  # If no history found for this UID
                        messagebox.showinfo("History", "No history found for this card.")
                else:  # If data is not a list or does not match expected structure
                    messagebox.showinfo("History", "Invalid data format in file.")
        except FileNotFoundError:
            messagebox.showinfo("History", "Data file not found.")


    def start_reading(self, event=None):
        cardmonitor = CardMonitor()
        cardmonitor.addObserver(self.nfc_observer)
        self.lift()
        messagebox.showinfo("NFC Reader", "Waiting for card...")

    def update_default_uid(self):
        default_uid_value = self.nfc_observer.get_uid()
        self.entry_uid.delete(0, tk.END)
        self.entry_uid.insert(0, str(default_uid_value))
        self.after(1000, self.update_default_uid)

    def register_card(self):
        name = self.entry_name.get()
        uid = self.entry_uid.get()
        student_id = self.entry_student_id.get()
        email = self.entry_email.get()
        full_name = self.entry_full_name.get()
        points = int(self.entry_points.get())  # Retrieve points

        if name and uid and student_id and full_name:
            if email.endswith("@ku.th"):
                # Check if points are set to 0
                if points == 0:
                    self.nfc_observer.register_card_data(name, uid, student_id, email, full_name, points)
                else:
                    messagebox.showerror("Error", "Points must be set to 0 during registration.")
            else:
                messagebox.showerror("Error", "Invalid email. Email must end with '@ku.th'.")
        else:
            messagebox.showerror("Error", "Please enter all required information.")


    def top_up_balance(self):
        self.nfc_observer.top_up_balance(self.entry_uid.get())

# Create the main Tkinter window
root = NFCRegistrationWindow('card_data.json')

# Run the Tkinter event loop
root.mainloop()