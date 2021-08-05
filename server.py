import socket
import threading

#LocalHost
host = '127.0.0.1'
#Choosing unreserved port
port = 12346

#socket initialization, IPv4 protocol domain, TCP communication type
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding host and port(socket address) to socket
server.bind((host, port))

#listens for 10 active connections. This number can be increased as per convenience
server.listen(10)

print("Server is Up!")
print("Waiting for connections")

clients = []
usernames = []

def broadcast(message, c):
    # broadcast function declaration
    for client in clients:
        # broadcast msg to every clients except the sender client
        if(client != c):
                client.send(message)

def handle(client):
    while True:
        # recieving valid messages from client
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} left!'.format(username).encode('ascii'), "")
            usernames.remove(username)
            break

def receive():
    # accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('UserName'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        usernames.append(nickname)
        clients.append(client)
        print("User is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'), "")
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()