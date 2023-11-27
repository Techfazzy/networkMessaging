import socket
import threading
import datetime


# Connection information
ip = "10.36.19.153"
port = 55555

# Start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((ip, port))
except socket.error as e:
    str(e)
server.listen()
print("Waiting for a connection, Server Started")

# Arrays for clients and usernames
clients = []
usernames = []


# Sending a message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling messages from clients
def handle(client):
    while True:
        try:
            # Broadcast the message
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} left!'.format(username).encode('ascii'))
            usernames.remove(username)
            break


# Receiving function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('USER'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        # Add datetime
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Print And Broadcast Nickname and Time
        print("Nickname is {}".format(username))
        broadcast("{} joined on".format(username).encode('ascii'))
        broadcast("{} ".format(date_time).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
