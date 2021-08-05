import socket
import threading                                                #Libraries import

host = '127.0.0.1'                                                      #LocalHost
port = 7976                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen(10)

clients = []
nicknames = []

def broadcast(message, c):                                                 #broadcast function declaration
    for client in clients:
        if(client != c):
                client.send(message)

def handle(client):
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            broadcast(message, client)
        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'), "")
            nicknames.remove(nickname)
            break

def receive():                                                          #accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'), "")
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()