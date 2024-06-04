#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

#funzione per la ricezione dei messaggi e controllo connessione client
def receive_msg():
    while True:
        try:
            msg=client_socket.recv(BUFSIZ).decode("utf-8")
            msg_list.insert(tkt.END, msg)
        except OSError:
            print("Client disconnesso dal server")
            break

#funzione per inviare messaggi dal client
def send_msg (event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg,"utf-8"))
        
#funzione che definisce il comportamento alla chiusura della chat
def on_closing_window(event=None):
    finestra.destroy()
    client_socket.close()
    
#gui fatta con tkinter
finestra = tkt.Tk()
finestra.title("Chat Elaborato")

msg_frame = tkt.Frame(finestra)
my_msg = tkt.StringVar()
my_msg.set(" ")
scrollbar = tkt.Scrollbar(msg_frame)
msg_list = tkt.Listbox(msg_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
msg_frame.pack()

entry_field = tkt.Entry(finestra, textvariable=my_msg)
entry_field.bind("<Return>", send_msg)

entry_field.pack()
send_button = tkt.Button(finestra, text="Invio", command=send_msg)
send_button.pack(side=tkt.BOTTOM,padx=5)
exit_button = tkt.Button(finestra, text="Esci", command=on_closing_window)
exit_button.pack(side=tkt.BOTTOM, padx=5)

finestra.protocol("WM_DELETE_WINDOW", on_closing_window)
   

HOST = input('Inserire il Server host: ')
if not HOST:
    HOST='127.0.0.1'
if HOST != '127.0.0.1':
    print("Non esiste questo server host!")
PORT = input('Inserire la porta del server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


receive_thread = Thread(target=receive_msg)
receive_thread.start()

tkt.mainloop()
