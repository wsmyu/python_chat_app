import socket
import tkinter as tk
import threading
from tkinter import filedialog, scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 4096


DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
WHITE = "white"
FONT = ("Helvetica", 17)
SMALL_FONT = ("Helvetica", 13)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)

      # Insert the message at the end of the text box
    message_box.insert(tk.END, message + '\n')

     # Set the message box back to disabled state to prevent modification
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        username = username_textbox.get().strip()
        if username:
            client.sendall(username.encode())
            threading.Thread(target=receive_messages, args=(client,)).start()
        else:
            messagebox.showerror("Username Error", "Username cannot be empty")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

def receive_messages(client):
    while True:
        message = client.recv(BUFFER_SIZE).decode('utf-8')
        if message.startswith("FILE RECEIVED:"):
            filename = message.split("~")[1]
            add_message(f"[SERVER] File received: {filename}")
        else:
            add_message(message)


def send_message():
    
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def send_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        filename = file_path.split("/")[-1]
        client.sendall(f"FILE:{filename}".encode())
        with open(file_path, 'rb') as f:
            bytes = f.read()
            file_size = len(bytes)
            client.sendall(str(file_size).encode())
            client.sendall(bytes)




# GUI setup
root = tk.Tk()
root.geometry("600x600")
root.title("Chat Application")
root.resizable(False, False)
root.config(bg=DARK_GREY)

top_frame = tk.Frame(root, bg=DARK_GREY, height=100)
top_frame.pack(fill=tk.X, padx=20, pady=10)

middle_frame = tk.Frame(root, bg=WHITE)
middle_frame.pack(fill=tk.BOTH, expand=True, padx=20)

bottom_frame = tk.Frame(root, bg=DARK_GREY, height=100)
bottom_frame.pack(fill=tk.X, padx=20, pady=10)

username_label = tk.Label(top_frame, text="Username:", bg=DARK_GREY, fg=WHITE, font=FONT)
username_label.pack(side=tk.LEFT)

username_textbox = tk.Entry(top_frame, bg=MEDIUM_GREY, fg=WHITE, font=FONT)
username_textbox.pack(side=tk.LEFT, fill=tk.X, expand=True)

username_button = tk.Button(top_frame, text="Connect", bg=MEDIUM_GREY, fg=WHITE, font=SMALL_FONT, command=connect)
username_button.pack(side=tk.LEFT, padx=10)

message_textbox = tk.Entry(bottom_frame, bg=MEDIUM_GREY, fg=WHITE, font=FONT)
message_textbox.pack(side=tk.LEFT, fill=tk.X, expand=True)

send_button = tk.Button(bottom_frame, text="Send", bg=MEDIUM_GREY, fg=WHITE, font=SMALL_FONT, command=send_message)
send_button.pack(side=tk.LEFT, padx=10)

send_file_button = tk.Button(bottom_frame, text="Send File", bg=MEDIUM_GREY, fg=WHITE, font=SMALL_FONT, command=send_file)
send_file_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, bg=WHITE, fg=DARK_GREY, font=SMALL_FONT, state=tk.DISABLED)
message_box.pack(fill=tk.BOTH, expand=True)

# main function
def main():
    root.mainloop()
    
if __name__ == '__main__':
    main()