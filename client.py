import socket
import threading

# Choosing a username
username = input("Choose your username: ")

# Connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("10.36.19.153", 55555))


# Listening to the server and sending the username
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            # Close connection since there is an error
            print("An error occured!")
            client.close()
            break


# Sending messages to the server
def write():
    while True:
        message = '{}: {}'.format(username, input(''))
        client.send(message.encode('ascii'))


# Start threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()