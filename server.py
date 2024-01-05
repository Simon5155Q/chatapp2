from threading import Thread
import socket
ip = "127.0.0.1"
port = 5500
server = None
clients = {}
buffersize = 4096

def setup():
    global server
    global ip
    global port
    global clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(10)
    print("server started")
    acceptClient()

def acceptClient():
    global server
    global clients
    while True:
        client,address = server.accept()
        print(client, address)
        clientName = client.recv(4096).decode()
        clients[clientName] = {
            "client": client,
            "address": address,
            "connectedwith": "",
            "filename":"" ,
            "filesize":4096
        }
        print(clientName)
        thread2 = Thread(target=handleClients, args=(client, clientName))
        thread2.start()

def handleClients(client, clientname):
    global clients
    global server
    global buffersize
    client.send("welcome to the chat".encode("utf-8"))
    while True:
        try:
            buffersize = clients[clientname]["filesize"]
            details = server.recv(buffersize)
            print(details, "3")
            if(details):
                print(details, "2")
                handlemsg(client, details, clientname)
        except:
            pass

def handlemsg(client, details, clientname):
    print(details, "1")
    if(details == "showlist"):
        handlelist(client)

def handlelist(client):
    print(client)
    global clients
    clientcount=0
    for i in clients:
        clientcount+=1
        clientaddress = clients[i]["address"][0]
        connectedwith = clients[i]["connectedwith"]
        message = ""
        if(connectedwith):
            message = f"{clientcount}, {i}, {clientaddress}, connected with, {connectedwith}, tiul, \n"
        else:
            message = f"{clientcount}, {i}, {clientaddress}, available, tiul, \n"
        client.send(message.encode())
        print(message)

thread1 = Thread(target=setup)
thread1.start()


