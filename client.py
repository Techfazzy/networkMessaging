import socket
import threading
import datetime
import colorama
from colorama import Fore, init, Style

init()
# Choosing a username
username = input("Choose your username: ")

# Choose a color
color = input("Choose your color (R, B, G, W): ")

# Connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("10.36.19.153", 55555))


# Listening to the server and sending the username
def receive():
    global color
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(username.encode('ascii'))
            else:
                if color == 'R':
                    color = Fore.RED
                elif color == 'B':
                    color = Fore.BLUE
                elif color == 'G':
                    color = Fore.GREEN
                else:
                    color = Fore.WHITE

                print_with_color(s=message, color=color)
        except:
            # Close connection since there is an error
            print("An error occurred!")
            client.close()
            break


# Sending messages to the server
def write():
    while True:
        # Add datetime
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = '{} {}: {}'.format(username, [date_time], input(''))
        client.send(message.encode('ascii'))


def print_with_color(s, color):
    """Utility function wrapping the regular print() function
    but with colors and brightness"""
    print(f"{color}{s}{Style.RESET_ALL}")


# Start threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
