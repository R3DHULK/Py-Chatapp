import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Lists to keep track of connected clients and their usernames
clients = []
usernames = []

# Broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle messages from clients
def handle(client):
    while True:
        try:
            # Receive message from client
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove and close the client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} left the chat!'.encode('utf-8'))
            usernames.remove(username)
            break

# Accept and handle new clients
def accept_connections():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # Request and store the client's username
        client.send('NAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        # Notify everyone about the new connection
        print(f'Username is {username}!')
        broadcast(f'{username} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        # Start handling the client's messages
        client.send('You are now connected!'.encode('utf-8'))
        client_thread = threading.Thread(target=handle, args=(client,))
        client_thread.start()

# Start accepting connections
print('Server is running...')
accept_connections()
