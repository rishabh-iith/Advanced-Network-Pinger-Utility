import time
import socket
import sys
import struct

# Function to ping the server N times
def send_udp_packets(server_address, N):
    c_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket for sending pings
    c_soc.settimeout(1)  # Set 1-second timeout for responses

    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)  # Raw socket for ICMP errors
    icmp_socket.settimeout(1)  # Timeout to capture ICMP responses

    l_p = 0  # Lost packets

    cnt_rtt = 0 #Variable to count the total number of rtt values
    total_rtt = 0 #Variable to store the total rtt value
    max_rtt = 0 #Variable to store the maximum rtt value
    min_rtt = float('inf') #Variable to store the minimum rtt value

    for i in range(1, N + 1):
        message = f"ping {i} {time.time()}"

        try:
            # Send the ping message via UDP
            start_time = time.time()
            c_soc.sendto(message.encode(), server_address)

            # Wait for the UDP response (1 second timeout)
            response, _ = c_soc.recvfrom(1024)
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
            # Handle timeout if no UDP response is received within 1 second
            print(f"Request timed out for the packet {i}")
            l_p += 1

            # After UDP timeout, attempt to capture an ICMP error response
            try:
                icmp_response, _ = icmp_socket.recvfrom(1024) #Receive the icmp response from raw socket
                icmp_header = icmp_response[20:28]  # ICMP header starts after the IP header
                icmp_type, code, checksum, packetID, packetSequence = struct.unpack('bbHHh', icmp_header) #Get the icmp type and code for error identification from the icmp header

                if icmp_type == 3:  # Destination Unreachable
                    if code == 0:
                        icmp_error_message = "Destination Network Unreachable" #For icmp type=3 and code=0, the error is Destination Network Unreachable
                    elif code == 1:
                        icmp_error_message = "Destination Host Unreachable" #For icmp type=3 and code=1, the error is Destination Host Unreachable
                    elif code ==3:
                        icmp_error_message = "Destination Port Unreachable" #For icmp type=3 and code=3, the error is Destination Host Unreachable
                    else:
                        icmp_error_message = "Unknown Destination Unreachable Error" #For any unknown icmp code 
                else:
                    icmp_error_message = f"Unknown ICMP Error: Type={icmp_type}, Code={code}" #For any unknown icmp type

                if icmp_error_message:
                    print(f"Received ICMP error for packet {i}: {icmp_error_message}")
            except socket.timeout:
                # No ICMP error message received within the timeout
                print(f"No ICMP error message for packet {i}")

    packet_l_r = (l_p / N) * 100  # Packet loss rate

    if cnt_rtt: #If we have atleast 1 rtt then we will print the statistics of ping requests otherwise no packet is received
        print(f"\n--- Ping Statistics ---")
        print(f"Packets: Sent = {N}, Received = {N - l_p}, Lost = {l_p} ({packet_l_r:.1f}% loss)") #Printing the count of packets sent, packets received, packets lost, and percentage of packets lost
        print(f"Min RTT = {min_rtt:.3f} ms, Max RTT = {max_rtt:.3f} ms, Avg RTT = {(total_rtt / cnt_rtt):.3f} ms") #Printing the maximum rtt value, minimum rtt value and average rtt value
    else:
        print("\nNo packets were received. All requests timed out.")

    c_soc.close() #Closing the client socket
    icmp_socket.close() #Closing the icmp raw socket

server_ip = '127.0.0.1'
server_port = 11001
N = int(input("Enter the number of pings: "))#Number of ping requests that client will send to server
address = (server_ip, server_port) #Address where we will send the udp packet
send_udp_packets(address, N)
