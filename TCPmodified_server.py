import random
import socket
import threading

# Create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 11000))

print("Server is running....")

def handle_client(conn, addr):
    while True:
        try:
            message = conn.recv(1024).decode()
            response_message = message.upper()
            conn.send(response_message.encode())

        except ConnectionResetError:
            break  # Handle if the client unexpectedly closes the connection

    conn.close()

def start(): 
    serverSocket.listen()
    while True:  # Listen until the server is manually stopped
        conn, addr = serverSocket.accept() #Accepting the connection from clients
        print(f"Ping received from {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #Created thread for handling multiple connections
        thread.start() #Starting the thread for new connections

start()
