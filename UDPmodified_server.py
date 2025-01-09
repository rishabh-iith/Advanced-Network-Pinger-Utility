import random
from socket import *

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 11001))

while True:
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    #the server responds with the capitalized message
    print(f"Ping received from {address}")
    message = message.upper()
    serverSocket.sendto(message, address)
