#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#funzione per accettare la connessione del client
def handle_connections():
    while True:
        try:
            client_socket, client_address = SERVER.accept()
            print("%s:%s si è collegato." % client_address)
            client_socket.send(bytes("Benvenuto! Digita il tuo nome: ", "utf8"))
            try:
                name=client_socket.recv(BUFSIZ).decode("utf-8")
                addresses[client_socket]= client_address
                clients[client_socket]=name
                msg = "%s si è unito all chat!" % name
                broadcast(bytes(msg, "utf8"))
                Thread(target=handle_clients, args=(client_socket,name)).start()
            except:
                print("Errore nella connessione del client")
        except:
            print("Errore durante l'accettazione della connessione del client")
        
        
#Funzione che gestisce la connessione dei client al server
def handle_clients (client_socket, name):
     while True:
        try:
            msg = client_socket.recv(BUFSIZ)
            broadcast(msg, name+": ")
        except ConnectionResetError:
            print("Client disconnesso")
            del clients[client_socket]
            broadcast(bytes("%s ha abbandonato la Chat." % name, "utf8"))
            client_socket.close()
            break
           
#funzione per mandare messaggi a tutti gli utenti della chat 
def broadcast (msg, sender=""):
    for utente in clients:
        utente.send(bytes(sender,"utf-8")+msg)
            
        
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    try:
        SERVER.listen(5)
        print ("Server in ascolto in attesa di connessioni: ")
        ACCEPT_THREAD = Thread(target=handle_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()
    except:
        print ("Errore nell avvio del server")
        exit()

    
        
