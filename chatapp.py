import socket
import threading

# Client configuration
HOST = '127.0.0.1'
PORT = 5555

# Request and store the client's username
username = input('Enter your username: ')

# Create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Function to receive and print messages from the server
def receive():
    while True:
        try:
            # Receive message from server
            message = client.recv(1024).decode('utf-8')
            if message == 'NAME':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            # Close the client
            print('An error occurred!')
            client.close()
            break

# Function to send messages to the server
def send():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('utf-8'))

# Start receiving and sending messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
