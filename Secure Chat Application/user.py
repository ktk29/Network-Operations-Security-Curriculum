import socket
import rsa
import threading
import re

import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


class User:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", 9090))

        self.public_key, self.private_key = rsa.newkeys(1024)

        self.server_key = socket.recv(1024)
        self.socket.send(self.public_key.save_pkcs1("PEM"))

        msg = tkinter.Tk()
        msg.withdraw()

        self.name = simpledialog.askstring("Name", "Please enter your name", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.config(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.chat_label.config(font=("Arial", 15))
        self.chat_label.pack(padx=20, pady=5)

        self.msg_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.msg_label.config(font=("Arial", 15))
        self.msg_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.configure(font=("Arial", 15))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.mainloop()
        self.win.protocol("WM_DELETE_WINDOW", self.stop())

    def input_validation(self, message):
        # removing dodgy characters from the message
        sanitized_string = re.sub(r"[;\\'\"]", "", message)
        # print error to console
        if not sanitized_string.isalnum():
            if self.gui_done:
                self.text_area.config(state="normal")
                self.text_area.insert('end', "Invalid message. Message will not send.")
                self.text_area.yview('end')
                self.text_area.config(state="disabled")
            return False
        return sanitized_string

    def write(self):
        message = f"{self.name}: {self.input_area.get('1.0', 'end')}"
        message = self.input_validation(message)
        self.input_area.delete('1.0', 'end')
        #only send if valid message
        if not message:
            self.socket.send(rsa.encrypt(message.encode(), self.server_key))

    def stop(self):
        self.running = False
        self.win.destroy()
        self.socket.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = rsa.decrypt(self.socket.recv(1024), self.private_key).decode()
                if message == "name":
                    self.socket.send(rsa.encrypt(self.name.encode(), self.server_key))

                else:
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state="disabled")
            except ConnectionAbortedError:
                print("i gave up")
                self.stop()

            except:
                print("i gave up here")
                self.stop()


user = User()
