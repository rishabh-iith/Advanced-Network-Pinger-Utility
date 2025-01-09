from socket import *  # Import necessary functions and constants from the socket module
import os  # To access system functionalities like getting process ID
import sys  # For system-specific parameters and functions
import struct  # For working with C-style data structures
import time  # For timing purposes (sending/receiving packets)
import select  # To wait for I/O completion
import statistics  # For calculating average and other statistics

# Constants for ICMP types
ICMP_ECHO_REQUEST = 8  # ICMP type for Echo Request
ICMP_ECHO_REPLY = 0    # ICMP type for Echo Reply

# Function to calculate the checksum of the ICMP packet
def checksum(source_string):
    csum = 0
    countTo = (len(source_string) // 2) * 2  # Process in 16-bit chunks
    count = 0

    # Loop to sum up all 16-bit words
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        csum += thisVal
        csum &= 0xffffffff  # Keep the result in 32 bits
        count += 2

    # Add left-over byte if the total length is odd
    if countTo < len(source_string):
        csum += source_string[len(source_string) - 1]
        csum &= 0xffffffff

    # Carry over any overflow bits
    csum = (csum >> 16) + (csum & 0xffff)
    csum += (csum >> 16)
    
    # One's complement and finalize the checksum
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)  # Convert to network byte order (big-endian)
    return answer

# Function to receive a ping response (ICMP Echo Reply)
def receiveOnePing(mySocket, ID, sequence, timeout, destAddr):
    timeLeft = timeout  # Timeout countdown
    while True:
        startedSelect = time.time()  # Mark time before select call
        # Wait for data to be available on the socket (up to `timeLeft` seconds)
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)  # Time spent waiting
        
        # If no data was received within the timeout period, return timeout message
        if whatReady[0] == []:
            return None, "Request timed out."

        # Record the time of reception
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)  # Receive the packet from the socket
        
        # Extract the ICMP header (bytes 20-28 of the IP packet)
        icmpHeader = recPacket[20:28]
        # Unpack the ICMP header fields
        icmpType, code, checksum, packetID, packetSequence = struct.unpack("bbHHh", icmpHeader)

        # Check if the received packet is an ICMP Echo Reply and the packet ID matches
        if icmpType == ICMP_ECHO_REPLY and code == 0 and packetID == ID and packetSequence == sequence:
            # Extract the time the packet was sent (which is stored in the data part)
            dataSize = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + dataSize])[0]
            
            # Extract the Time-To-Live (TTL) from the IP header (8th byte)
            ttl = struct.unpack("B", recPacket[8:9])[0]
            
            # Calculate the Round Trip Time (RTT)
            rtt = timeReceived - timeSent
            
            # Ensure the data matches between the request and reply
            sentData = recPacket[28:]  # Data in the reply
            if sentData == struct.pack("d", timeSent):
                # Return details of the reply
                return rtt, f"Reply from {addr[0]}: bytes={len(recPacket)} rtt={rtt*1000:.3f}ms TTL={ttl} Sequence Number={packetSequence}"
            else:
                return None, "Data mismatch between request and reply"
        
        # Handle ICMP error codes
        elif icmpType == 3:  # Destination unreachable
            if code == 0:
                return None, "Destination Network Unreachable"
            elif code == 1:
                return None, "Destination Host Unreachable"
            elif code ==3:
                return None, "Destination Port Unreachable"
            # Add more error cases as needed
        else:
            return None, f"Error: ICMP Type {icmpType}, Code {code}"
        
        # Decrease the remaining time
        timeLeft -= howLongInSelect
        # If the remaining time is up, return a timeout message
        if timeLeft <= 0:
            return None, "Request timed out."

# Function to send a single ping (ICMP Echo Request)
def sendOnePing(mySocket, destAddr, ID, sequence):
    # Create an ICMP Echo Request header (type 8, code 0, and a dummy checksum for now)
    myChecksum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    data = struct.pack("d", time.time())  # Add the current time as the payload

    # Calculate the correct checksum for the packet
    myChecksum = checksum(header + data)

    # Correct the checksum in the header
    if sys.platform == 'darwin':  # For macOS, the checksum needs to be handled differently
        myChecksum = htons(myChecksum) & 0xffff
    else:  # For other platforms, the regular checksum works
        myChecksum = htons(myChecksum)

    # Recreate the header with the correct checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    packet = header + data  # Combine the header and the payload

    # Send the packet to the destination address
    mySocket.sendto(packet, (destAddr, 1))  # The '1' is the protocol number for ICMP

# Function to perform one ping
def doOnePing(destAddr, timeout, sequence):
    icmp = getprotobyname("icmp")  # Get the protocol number for ICMP
    mySocket = socket(AF_INET, SOCK_RAW, icmp)  # Create a raw socket for ICMP

    myID = os.getpid() & 0xFFFF  # Get the process ID and limit it to 16 bits

    # Send the ICMP Echo Request
    sendOnePing(mySocket, destAddr, myID, sequence)
    # Receive the ICMP Echo Reply (or timeout)
    delay = receiveOnePing(mySocket, myID, sequence, timeout, destAddr)

    mySocket.close()  # Close the socket after use
    return delay

# Ping function that handles multiple ping requests
def ping(host, count=10, timeout=1):
    dest = gethostbyname(host)
    print(f"Pinging {dest} using Python:")
    print("")

    rtt_times = []
    packets_received = 0

    for i in range(count):
        delay, message = doOnePing(dest, timeout, i + 1)  # Increment sequence number for each request
        if delay:
            packets_received += 1
            rtt_times.append(delay)
        print(message)
        time.sleep(1)

    # RTT statistics
    if rtt_times:
        min_rtt = min(rtt_times) * 1000  # minimum rtt in ms
        max_rtt = max(rtt_times) * 1000  # maximum rtt in ms
        avg_rtt = statistics.mean(rtt_times) * 1000  # average rtt in ms
    else:
        min_rtt = max_rtt = avg_rtt = 0

    # Packet loss calculation
    packet_loss = ((count - packets_received) / count) * 100

    # Print summary
    print("\n--- Ping statistics ---")
    print(f"{count} packets transmitted, {packets_received} received, {packet_loss:.1f}% packet loss") #Printing the number of packets transmitted, received and percentage of packet loss
    print(f"rtt min = {min_rtt:.3f} ms, rtt avg = {avg_rtt:.3f} ms, rtt max = {max_rtt:.3f} ms") #Printing the minimum rtt, average rtt and maximum rtt

# Example call to ping google.com
ping("google.com", count=10)  # Ping google.com 5 times