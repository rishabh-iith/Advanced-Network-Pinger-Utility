# TCP Server and Client Ping Program

This project implements a simple TCP server and client using Python's socket library. The server listens for incoming TCP connections, processes ping messages, and sends responses back to the client. The client sends a specified number of ping messages to the server, measures the round-trip time (RTT) for each ping, and calculates statistics on the RTT.

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
  - Listens for TCP connections from clients.
  - Handles multiple client connections using threading.
  - Randomly drops 20% of the packets to simulate packet loss.
  - Responds with the message capitalized if the packet is not dropped.

- **Client**:
  - Sends a specified number of TCP ping requests to the server.
  - Measures the round-trip time (RTT) for each successful ping.
  - Prints the minimum, maximum, and average RTT and the packet loss rate.
  - Captures ICMP error messages using a raw socket if a TCP connection times out.

## Requirements

- Python 3.x
- A basic understanding of networking and sockets.
- Elevated privileges (e.g., running with `sudo`) may be required to capture ICMP errors for the client on some operating systems.

## Setup

1. **Save the Code**:
   - Save the server code as `tcp_server.py` and the client code as `tcp_client.py`.

2. **Ensure Python is Installed**:
   - Make sure Python 3.x is installed on your system.

## Usage

#### Running the Server:

1. Open a terminal.
2. Navigate to the directory where `tcp_server.py` is saved.
3. Run the server:
```bash
python3 tcp_server.py
```

*The server will start listening on the IP address `127.0.0.1` and port `11000`*

## Running the Client:
-Open another terminal.
-Navigate to the directory where tcp_client.py is saved.
-Run the client:
```bash
sudo python3 tcp_client.py
```
# Client-Side Configuration:

*Server Address*

The client connects to the server at `127.0.0.1:11000`. You can modify this in the client script if needed.

*Ping Count*

The client sends 20 ping requests by default, which can be changed by modifying the N variable in the script.

## Server Example Output on a Different Machine:
```python

Ping received from ('192.168.0.155', 53807)
Ping received from ('192.168.0.155', 53808)
Ping received from ('192.168.0.155', 53809)
Ping received from ('192.168.0.155', 53810)
Ping received from ('192.168.0.155', 53811)
Ping received from ('192.168.0.155', 53812)
Ping received from ('192.168.0.155', 53813)
Ping received from ('192.168.0.155', 53814)
Ping received from ('192.168.0.155', 53815)
Ping received from ('192.168.0.155', 53816)
Ping received from ('192.168.0.155', 53817)
Ping received from ('192.168.0.155', 53818)
Ping received from ('192.168.0.155', 53819)
Ping received from ('192.168.0.155', 53820)
Ping received from ('192.168.0.155', 53821)
Ping received from ('192.168.0.155', 53822)
Ping received from ('192.168.0.155', 53823)
Ping received from ('192.168.0.155', 53824)
Ping received from ('192.168.0.155', 53825)
Ping received from ('192.168.0.155', 53826)
```
## Client Example Output on a Different Machine:
```python
Enter the number of pings: 20
Received: PING 1 1726146326.979706
RTT for packet 1: 14.505 ms
Received: PING 2 1726146326.99436
RTT for packet 2: 11.329 ms
Received: PING 3 1726146327.005749
RTT for packet 3: 13.021 ms
Request timed out for the packet 4
No ICMP error message for packet 4
Received: PING 5 1726146329.021101
RTT for packet 5: 17.672 ms
Received: PING 6 1726146329.0388649
RTT for packet 6: 8.590 ms
Received: PING 7 1726146329.047503
RTT for packet 7: 13.830 ms
Received: PING 8 1726146329.061423
RTT for packet 8: 6.615 ms
Received: PING 9 1726146329.068089
RTT for packet 9: 11.093 ms
Received: PING 10 1726146329.079272
RTT for packet 10: 7.317 ms
Received: PING 11 1726146329.0866501
RTT for packet 11: 31.768 ms
Received: PING 12 1726146329.11853
RTT for packet 12: 11.641 ms
Received: PING 13 1726146329.130251
RTT for packet 13: 10.757 ms
Received: PING 14 1726146329.141071
RTT for packet 14: 8.501 ms
Request timed out for the packet 15
Request timed out for the packet 16
Received: PING 17 1726146333.15449
RTT for packet 17: 9.203 ms
Received: PING 18 1726146333.163775
RTT for packet 18: 9.743 ms
Received: PING 19 1726146333.173569
RTT for packet 19: 9.668 ms
Received: PING 20 1726146333.183271
RTT for packet 20: 18.041 ms
```

## Script Breakdown

**Server Script:**

1. Socket Setup: The server creates a TCP socket and binds it to the local address `127.0.0.1` and port `11000`.

2. Handling Multiple Clients: The server uses threading to handle multiple client connections simultaneously. For each new client, a new thread is created to handle that connection.

3. Packet Loss Simulation: The server simulates a 20% packet loss using the random.randint function to randomly decide whether to drop a packet.

**Client Script:**

1. TCP Socket Creation: The client creates a TCP socket for each ping request and connects to the server. It also handles timeouts and potential errors during the connection process.

2. Ping Loop: The client sends a ping message and calculates the RTT if a response is received. If no response is received within the timeout, the client logs the packet as lost.

3. RTT Statistics: After all pings are sent, the client calculates and prints the minimum, maximum, and average RTT, as well as the packet loss rate.

4. ICMP Error Handling: The client attempts to capture ICMP error messages using a raw socket if a TCP connection times out. This requires elevated privileges on some systems.

## Error Handling

The client handles the following types of errors:

-->Timeout: If the server does not respond within the 1-second timeout, the client prints that the packet was lost and moves on to the next ping.

-->ICMP Errors: If a packet is lost, the client attempts to capture ICMP error messages. These errors indicate network issues, such as unreachable destinations.

-->OSError Handling: If an OS-related error occurs, the client catches and prints the error number and its description.

## Notes

-Ensure the server is running and reachable at the correct IP address and port.

-The client script requires elevated privileges to capture ICMP error messages using raw sockets (e.g., using sudo on Linux).

-This project simulates packet loss for testing purposes.

## Modified TCP Server

- The TCP Server is modified to use multithreading in order to handle multiple clients concurrently.
- Multithreading in a TCP server is a technique used to handle multiple client connections simultaneously by creating a separate thread for each client connection. 
- This approach allows the server to manage multiple clients at the same time without blocking other connections, leading to improved performance and responsiveness, especially when dealing with concurrent clients.

- Steps involved in Multithreading in a TCP Server:
    -Main Server Thread: The start() function runs in the main thread and listens for incoming client connections.
    -New Client Connection: When a new client connects, a new thread is created to handle the communication with that client. This is done using threading.Thread.
    -Start Thread: The newly created thread starts running the handle_client function, which handles communication with the client.
    -Client Communication: Each thread handles one client. The server communicates with the client, potentially simulating packet loss and sending responses.
    -Main Thread Continues: Meanwhile, the main thread continues accepting more client connections and starting new threads, allowing the server to handle multiple clients concurrently.

- Run the following code in python to incorporate multithreading by creating new thread:
```python
thread = threading.Thread(target=handle_client, args=(conn, addr))
```

## Contact

For questions or contributions, please contact:

(mailto:cs24mtech14004@iith.ac.in)-- Ankush Chhabra <CS24MTECH14004 >
(mailto:sm24mtech11008@iith.ac.in)-- Rishabh Chaturvedi <SM24MTECH11008>
(mailto:cs24mtech11014@iith.ac.in)-- Jayanth Jatavath <CS24MTECH11014> 
