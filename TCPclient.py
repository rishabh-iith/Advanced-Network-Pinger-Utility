import errno
import socket
import time
import sys, os
import struct

# Function to ping the server N times using TCP
def tcp_ping_client(address, N):
    rtts = []
    l_p = 0  # Lost packets

    # Create a raw socket for ICMP error handling
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.settimeout(1)  # Set 1-second timeout for ICMP responses

    cnt_rtt = 0 #Variable to count the total number of rtt values
    total_rtt = 0 #Variable to store the total rtt value
    max_rtt = 0 #Variable to store the maximum rtt value
    min_rtt = float('inf') #Variable to store the minimum rtt value

    for i in range(1, N + 1):
        c_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
        try:
            # Record the start time
            start_time = time.time()

            # Connect to the server
            c_soc.connect(address)
            c_soc.settimeout(1)  # Set a timeout for the TCP connection

            message = f"ping {i} {time.time()}"
            c_soc.send(message.encode())  # Send ping message over TCP

            # Try to receive a TCP response
            response = c_soc.recv(1024)

            # Record the end time
            end_time = time.time()

            # Calculate RTT in milliseconds
            rtt = (end_time - start_time) * 1000
            total_rtt+=rtt  #Find the sum of all rtt values
            cnt_rtt+=1  #Find the total number of rtt values

            if max_rtt < rtt:#Find the maximum rtt
                max_rtt = rtt
            if min_rtt > rtt:#Find the minimum rtt
                min_rtt = rtt

            print(f"Received: {response.decode()}")
            print(f"RTT for packet {i}: {rtt:.3f} ms")

        except socket.timeout:
            # If TCP request times out, check for ICMP error
            print(f"Request timed out for packet {i}")
            l_p += 1

        # Catch OSError exceptions
        except OSError as e:
            # Check if the exception has an associated error number
            if e.errno:
                # Print the error number and the corresponding error message
                print(f"Error {e.errno}: {os.strerror(e.errno)}")
        finally:
            # Ensure the socket is closed, even if an exception occurs
            c_soc.close()

    # Calculate packet loss and RTT statistics
    packet_l_r = (l_p / N) * 100  # Packet loss rate

    if cnt_rtt: #If we have atleast 1 rtt then we will print the statistics of ping requests otherwise no packet is received
        print(f"\n--- Ping Statistics ---")
        print(f"Packets: Sent = {N}, Received = {N - l_p}, Lost = {l_p} ({packet_l_r:.1f}% loss)") #Printing the count of packets sent, packets received, packets lost, and percentage of packets lost
        print(f"Min RTT = {min_rtt:.3f} ms, Max RTT = {max_rtt:.3f} ms, Avg RTT = {(total_rtt / cnt_rtt):.3f} ms") #Printing the maximum rtt value, minimum rtt value and average rtt value
    else:
        print("\nNo packets were received. All requests timed out.")

    icmp_socket.close() #Closing the icmp socket

server_ip = '127.0.0.1'
server_port = 11000
N = int(input("Enter the number of pings:")) #Number of ping requests that client will send to server
address = (server_ip, server_port) #Address where we will send the tcp packet

tcp_ping_client(address, N)