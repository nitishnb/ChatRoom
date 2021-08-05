import socket
import threading

username = raw_input("UserName : ")

#socket initialization, IPv4 protocol domain, TCP communication type
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connecting client to server
client.connect(('127.0.0.1', 7976))

def receive():
    while True:
        # making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'UserName':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            # case on wrong ip/port details
            print("An error occured!")
            client.close()
            break

#message layout
def write():
    while True:
        message = '{}: {}'.format(username, raw_input(''))
        client.send(message.encode('ascii'))

#receiving multiple messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

#sending messages
write_thread = threading.Thread(target=write)
write_thread.start()