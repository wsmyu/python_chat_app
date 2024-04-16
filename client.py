import socket
import tkinter as tk
import threading
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 12345

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
WHITE = "white"
FONT = ("Helvetica", 17)
SMALL_FONT = ("Helvetica", 13)

connected_username = ""

# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)

      # Insert the message at the end of the text box
    message_box.insert(tk.END, message + '\n')

     # Set the message box back to disabled state to prevent modification
    message_box.config(state=tk.DISABLED)

def connect():
    global connected_username  # Declare that we will use the global variable

    # try except block
    try:
        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        # Send the username to the server if it's not empty
        client.sendall(username.encode())
        # Set the connected_username variable to the entered username
        connected_username = username  # Set the connected_username variable
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")
        
    # Start a new thread to listen for messages from the server
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

def send_message():
     # Check if the username is empty
    if not connected_username:
        messagebox.showinfo("Please Enter Username", "[SERVER] Please enter your username to connect to the server first")
        return
    
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address
client_socket.connect(('127.0.0.1', 12345))

# GUI setup
root = tk.Tk()
root.geometry("600x600")
root.title("Chat Application")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=WHITE)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=SMALL_FONT, bg=DARK_GREY, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=SMALL_FONT, bg=DARK_GREY, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=WHITE, fg=DARK_GREY, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

# main function
def main():
    root.mainloop()
    
if __name__ == '__main__':
    main()