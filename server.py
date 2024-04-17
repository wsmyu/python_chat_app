import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
LISTENER_LIMIT = 5  # Maximum number of clients the server can listen to simultaneously
BUFFER_SIZE = 4096  # Standard buffer size for network operations
active_clients = [] # List of all currently connected users

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):
    while True:
        message = client.recv(BUFFER_SIZE).decode('utf-8')
        if message:
            if message.startswith("FILE:"):
                handle_file_reception(client, message[5:], username)
            else:
                final_msg = f"{username}~{message}"
                send_messages_to_all(final_msg)
        else:
            print(f"Empty message received from {username}")
            break

def handle_file_reception(client, filename, username):
    file_length = int(client.recv(BUFFER_SIZE).decode('utf-8'))
    with open(filename, 'wb') as f:
        bytes_read = 0
        while bytes_read < file_length:
            bytes = client.recv(BUFFER_SIZE)
            if not bytes:
                break
            f.write(bytes)
            bytes_read += len(bytes)
    send_messages_to_all(f"FILE RECEIVED: {username}~{filename}")

# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    username = client.recv(BUFFER_SIZE).decode('utf-8')
    if username:
        active_clients.append((username, client))
        send_messages_to_all("SERVER~" + f"{username} joined the chat")
        threading.Thread(target=listen_for_messages, args=(client, username)).start()
    else:
        print("Client username is empty")

# Main function
def main():

    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)
    print("Waiting for connections...")


    # This while loop will keep listening to client connections
    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        # Start a new thread to handle the client connection
        # The client_handler function is responsible for handling the client connection.
        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()