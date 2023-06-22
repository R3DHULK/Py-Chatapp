import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import socket

# Client configuration
HOST = '127.0.0.1'
PORT = 5555
BUFFER_SIZE = 4096

# Create the main window
window = tk.Tk()
window.title("Chat App")

# Create a scrolled text widget to display messages
chat_box = scrolledtext.ScrolledText(window, height=20, width=50)
chat_box.configure(state='disabled')
chat_box.pack(padx=10, pady=10)

# Create an entry widget for user input
entry_box = tk.Entry(window, width=50)
entry_box.pack(padx=10, pady=10)

# Create a button for sending messages
send_button = tk.Button(window, text="Send", command=lambda: send())
send_button.pack(padx=10, pady=5)

# Function to handle receiving messages from the server
def receive():
    while True:
        try:
            # Receive message from server
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            chat_box.configure(state='normal')
            chat_box.insert(tk.END, message + '\n')
            chat_box.configure(state='disabled')
            chat_box.see(tk.END)
        except:
            # Close the client
            print('An error occurred!')
            client_socket.close()
            break

# Function to send messages to the server
def send(event=None):
    message = entry_box.get()
    entry_box.delete(0, tk.END)
    client_socket.send(message.encode('utf-8'))

# Function to handle the window close event
def on_closing(event=None):
    client_socket.close()
    window.destroy()

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Start receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Set up event bindings
window.protocol("WM_DELETE_WINDOW", on_closing)
window.bind('<Return>', send)

# Start the main loop
tk.mainloop()
