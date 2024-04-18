import socket
import tkinter as tk
import threading
import time
from tkinter import filedialog, scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 4096

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
WHITE = "white"
FONT = ("Helvetica", 12)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"[{timestamp}] {message}"
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, formatted_message + '\n')
    message_box.see(tk.END)
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        username = username_textbox.get().strip()
        if username:
            client.sendall(username.encode())
            threading.Thread(target=receive_messages, args=(client,)).start()
            root.withdraw()  # Hide the username window
            chat_window.deiconify()  # Show the chat window
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
    if message.strip():
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
            file_data = f.read()
            client.sendall(str(len(file_data)).encode())
            client.sendall(file_data)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        client.close()  # Close the socket connection
        root.destroy()  # Close the username window

# GUI setup
root = tk.Tk()
root.geometry("300x100")
root.title("Username")
root.resizable(False, False)
root.config(bg=DARK_GREY)
root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closure event

username_label = tk.Label(root, text="Enter Username:", bg=DARK_GREY, fg=WHITE, font=FONT)
username_label.pack(pady=5)

username_textbox = tk.Entry(root, bg=MEDIUM_GREY, fg=WHITE, font=FONT)
username_textbox.pack(padx=10, pady=(0, 5), fill=tk.BOTH, expand=True)

connect_button = tk.Button(root, text="Connect", bg=MEDIUM_GREY, fg=WHITE, font=FONT, command=connect)
connect_button.pack(pady=5)

# Chat window
chat_window = tk.Toplevel()
chat_window.geometry("600x500")
chat_window.title("Chat Application")
chat_window.resizable(False, False)
chat_window.config(bg=DARK_GREY)
chat_window.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closure event

message_frame = tk.Frame(chat_window, bg=DARK_GREY)
message_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(10, 5))

message_textbox = tk.Entry(message_frame, bg=MEDIUM_GREY, fg=WHITE, font=FONT)
message_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

send_button = tk.Button(message_frame, text="Send", bg=MEDIUM_GREY, fg=WHITE, font=FONT, command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

send_file_button = tk.Button(message_frame, text="Send File", bg=MEDIUM_GREY, fg=WHITE, font=FONT, command=send_file)
send_file_button.pack(side=tk.LEFT, padx=5)

message_box = scrolledtext.ScrolledText(chat_window, bg=WHITE, fg=DARK_GREY, font=FONT, state=tk.DISABLED)
message_box.pack(fill=tk.BOTH, expand=True)

chat_window.withdraw()  # Hide the chat window initially

# Main function
def main():
    root.mainloop()

if __name__ == '__main__':
    main()
