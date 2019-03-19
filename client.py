#!/bin/env python3
'''Script for Tkinter GUI chat client.'''

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter


# This handles recieving messages.
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode('utf-8')
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


# Handles sending messages.
def send(event=None):  # Event is passed by binders.
    msg = my_msg.get()
    my_msg.set('')  # Clears input field.
    client_socket.send(bytes(msg, 'utf-8'))
    if msg == '{quit}':
        client_socket.close()
        top.quit()


# Handles when the window is closed.
def on_closing(event=None):
    my_msg.set('{quit}')
    send()


# Initiates tkinter frame and adds Chatter as title.
top = tkinter.Tk()
top.title('Chatter')

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set('Type your messages here.')
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past \
                                               # messages.

msg_list = tkinter.Listbox(messages_frame, height=15, width=50,
    yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind('<Return>', send)
entry_field.pack()
send_button = tkinter.Button(top, text='Send', command=send)
send_button.pack()

top.protocol('WM_DELETE_WINDOW', on_closing)

''' Asks for host and port and handles connecting to server'''
HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000 # Default port Value.
else:
    PORT = int(PORT)

BUFSIZE = 1024  # 1GB
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

recieve_thread = Thread(target=receive)
recieve_thread.start()
tkinter.mainloop()  # Starts GUI execution.
