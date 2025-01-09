import random
from socket import *

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('192.168.0.155', 11000))

while True:
    # Generate a random number between 1 to 10 (both inclusive)
    rand = random.randint(1, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    if rand > 8:
        # Simulate packet loss by not sending a response
        print("Packet loss")
        continue

    # Otherwise, the server responds with the capitalized message
    print(f"Ping received from {address}")
    message = message.upper()
    serverSocket.sendto(message, address)
