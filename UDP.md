# UDP Server and Client Ping Program

This project implements a simple UDP server and client using Python's socket library. The server listens for incoming UDP packets, processes them, and sends a response back to the client. The client sends a specified number of ping messages to the server, measures the round-trip time (RTT) for each ping, and calculates statistics on the RTT.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Example](#example)
- [Code Breakdown](#code-breakdown)
- [Error Handling](#error-handling)
- [Notes](#notes)
- [License](#license)

## Overview

The project consists of two parts:

- **Server**:
  - Listens for UDP packets sent by the client.
  - Randomly drops about 20% of the packets to simulate packet loss.
  - Responds to the client by capitalizing the received message.

- **Client**:
  - Sends a specified number of ping requests to the server.
  - Measures the round-trip time (RTT) for each successful ping.
  - Prints the minimum, maximum, and average RTT and the packet loss rate.
  - Prints the ICMP error if we get any

## Requirements

- Python 3.x
- A basic understanding of networking and sockets.
- Elevated privileges (e.g., running with `sudo`) may be required to capture ICMP errors for the client on some operating systems.

## Setup

1. **Save the Code**:
   - Save the server code as `server.py` and the client code as `client.py`.

2. **Ensure Python is Installed**:
   - Make sure Python 3.x is installed on your system.

## Usage

#### Running the Server:

1. Open a terminal.
2. Navigate to the directory where `server.py` is saved.
3. Run the server:
   ```bash
   python3 server.py

#### Client-Side Configuration:

- *Server Address*: The client connects to the server at 127.0.0.1:11000. You can modify this in the client script if needed.
- *Ping Count*: The client sends 20 ping requests by default, which can be changed by modifying the N variable in the script.

## Example
Sample Output from server:
```bash
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Packet loss
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Packet loss
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Packet loss
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)
Ping received from ('127.0.0.1', 61572)

Client Example Output:
```bash
Enter the number of pings: 20
Received: PING 1 1726136613.864512
RTT for packet 1: 0.745 ms
Received: PING 2 1726136613.8653529
RTT for packet 2: 0.139 ms
Received: PING 3 1726136613.8655128
RTT for packet 3: 0.080 ms
Received: PING 4 1726136613.865608
RTT for packet 4: 0.073 ms
Received: PING 5 1726136613.865695
RTT for packet 5: 0.064 ms
Request timed out for packet 6
No ICMP error message for packet 6
Received: PING 7 1726136615.868084
RTT for packet 7: 0.525 ms
Received: PING 8 1726136615.868682
RTT for packet 8: 0.244 ms
Request timed out for packet 9
No ICMP error message for packet 9
Received: PING 10 1726136617.87137
RTT for packet 10: 0.455 ms
Received: PING 11 1726136617.871893
RTT for packet 11: 0.206 ms
Received: PING 12 1726136617.8721359
RTT for packet 12: 0.173 ms
Request timed out for packet 13
No ICMP error message for packet 13
Received: PING 14 1726136619.874775
RTT for packet 14: 0.488 ms
Received: PING 15 1726136619.875339
RTT for packet 15: 0.220 ms
Received: PING 16 1726136619.875607
RTT for packet 16: 0.194 ms
Received: PING 17 1726136619.875839
RTT for packet 17: 0.200 ms
Received: PING 18 1726136619.87608
RTT for packet 18: 0.151 ms
Received: PING 19 1726136619.876265
RTT for packet 19: 0.131 ms
Received: PING 20 1726136619.876423
RTT for packet 20: 0.144 ms

--- Ping Statistics ---
Packets: Sent = 20, Received = 17, Lost = 3 (15.0% loss)
Min RTT = 0.064 ms, Max RTT = 0.745 ms, Avg RTT = 0.249 ms

## Code Breakdown

**Server Code:**
1. Socket Setup: The server creates a UDP socket and binds it to the local address 127.0.0.1 and port 11000.

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('127.0.0.1', 11000))
    
2. Receiving and Responding: The server enters an infinite loop, waiting to receive messages from the client. It uses random.randint to simulate packet loss by not sending a response for 20% of the received messages.

rand = random.randint(1, 10)
message, address = serverSocket.recvfrom(1024)
if rand > 8:
    continue
message = message.upper()
serverSocket.sendto(message, address)

**Client Code:**
1. UDP Socket Creation: The client creates a UDP socket to send pings to the server and sets a timeout of 1 second for each response.

c_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c_soc.settimeout(1)

2. Ping Loop: The client sends a ping message to the server and calculates the RTT if a response is received. If no response is received within the timeout, the client logs the packet as lost.

for i in range(1, N + 1):
    start_time = time.time()
    c_soc.sendto(message.encode(), server_address)
    response, _ = c_soc.recvfrom(1024)
    end_time = time.time()
    rtt = (end_time - start_time) * 1000

3. ICMP Error Handling: If no UDP response is received, the client attempts to capture any ICMP error messages using a raw socket. This requires elevated privileges on some systems.

try:
    icmp_response, _ = icmp_socket.recvfrom(1024)
    icmp_header = icmp_response[20:28]
except socket.timeout:
    print(f"No ICMP error message for packet {i}")

4. RTT Statistics: After all pings are sent, the client calculates and prints the minimum, maximum, and average RTT, as well as the packet loss rate.

if cnt_rtt:
    print(f"Min RTT = {min_rtt:.3f} ms, Max RTT = {max_rtt:.3f} ms, Avg RTT = {(total_rtt / cnt_rtt):.3f} ms")

## Error Handling

The client handles the following types of errors:

**Timeout**
If the server does not respond within the 1-second timeout, the client prints that the packet was lost and moves on to the next ping.

**ICMP Errors**
If a packet is lost, the client attempts to capture ICMP error messages. These errors indicate network issues, such as unreachable destinations.

## Notes

-Ensure the server is running and reachable at the correct IP address and port.
-The client script requires elevated privileges to capture ICMP error messages using raw sockets (e.g., using sudo on Linux).
-This project simulates packet loss for testing purposes.

## Modified UDP Server:

- The UDP Server is modified to emulate packet loss at the network interface card (NIC) level by using tc (traffic control) netem utility in Linux.
- Since you are emulating losses at the NIC level, your server program no longer requires any code to simulate packet losses using randint( ) function and therefore modify it accordingly.

Run the following code in your Terminal window to emulate 20% packet loss:
```bash
sudo tc qdisc add dev wlp0s20f3 root netem loss 20%
```

## Troubleshooting

- **Timeouts**: If you experience high packet loss or timeouts, check the server's network and response handling.
- **Socket Errors**: Ensure that the server is running and listening on the correct address and port.

## Contact

For questions or contributions, please contact:

(mailto:cs24mtech14004@iith.ac.in)-- Ankush Chhabra <CS24MTECH14004 >
(mailto:sm24mtech11008@iith.ac.in)-- Rishabh Chaturvedi <SM24MTECH11008>
(mailto:cs24mtech11014@iith.ac.in)-- Jayanth Jatavath <CS24MTECH11014> 
