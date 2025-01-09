# ICMP Server and Client Ping Program

This part details the development of a ping client (client_part3.py) using ICMP to send echo requests and receive echo replies. The client application simulates ping functionality by sending ICMP Echo Requests and processing ICMP Echo Replies without fully adhering to the official RFC 1739 specification. 

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

The project consists of client side part:
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
   - Save the client code as `client.py`.

2. **Ensure Python is Installed**:
   - Make sure Python 3.x is installed on your system.

## Usage

#### Server-Side Configuration:
No Server Side Configuration as the functionality needed on the server side is built into almost all operating systems.
#### Client-Side Configuration:

- *Server Address*: The client connects to the server at `google.com`. You can modify this in the client script if needed.
- *Ping Count*: The client sends `10` ping requests by default, which can be changed by modifying the ping("google.com", count=10) function in the script.

## Example
Output from google.com when client pings it:
```bash
Reply from 142.250.193.142: bytes=36 rtt=28.735ms TTL=53 Sequence Number=1
Reply from 142.250.193.142: bytes=36 rtt=38.964ms TTL=53 Sequence Number=2
Reply from 142.250.193.142: bytes=36 rtt=35.492ms TTL=53 Sequence Number=3
Reply from 142.250.193.142: bytes=36 rtt=28.774ms TTL=53 Sequence Number=4
Reply from 142.250.193.142: bytes=36 rtt=27.496ms TTL=53 Sequence Number=5
Reply from 142.250.193.142: bytes=36 rtt=27.384ms TTL=53 Sequence Number=6
Reply from 142.250.193.142: bytes=36 rtt=27.445ms TTL=53 Sequence Number=7
Reply from 142.250.193.142: bytes=36 rtt=30.470ms TTL=53 Sequence Number=8
Reply from 142.250.193.142: bytes=36 rtt=29.049ms TTL=53 Sequence Number=9
Reply from 142.250.193.142: bytes=36 rtt=31.236ms TTL=53 Sequence Number=10

--- Ping Statistics ---
10 packets transmitted, 10 received, 0.0% packet loss
rtt min = 27.384 ms, rtt avg = 30.505 ms, rtt max = 38.964 ms
```

## Code Breakdown

**Server Code:**
No Server Code as the functionality needed on the server side is built into almost all operating systems.

**Client Code:**
1. ICMP Echo Reply Parsing: Added logic to parse the ICMP Echo Reply header in the receiveOnePing method, extracting the packet's ID, sequence number, and other fields. This ensures that only valid replies are processed.
```python
icmpType, code, checksum, packetID, packetSequence = struct.unpack("bbHHh", icmpHeader)
```

2. Round Trip Time (RTT) Calculation: Implemented functionality to calculate the RTT by recording the send and receive times of each ping request and response. This value is displayed for each ping. timeSent can be extracted from the received packet
```python
timeReceived = time.time()
timeSent = struct.unpack("d", recPacket[28:28 + dataSize])[0]        
rtt = timeReceived - timeSent
```

3. ICMP Error Handling: If no ICMP reply is received which matches the request ID and sequence number, the client attempts to capture any ICMP error messages. This requires elevated privileges on some systems.
```python
if icmpType == 3:
    if code == 0:
        return None, "Destination Network Unreachable"
    elif code == 1:
        return None, "Destination Host Unreachable"
    elif code ==3:
        return None, "Destination Port Unreachable"
else:
    return None, f"Error: ICMP Type {icmpType}, Code {code}"
```

4. RTT Statistics: After all pings are sent, the client calculates and prints the minimum, maximum, and average RTT, as well as the packet loss rate.
```python
if rtt_times:
    min_rtt = min(rtt_times) * 1000  # minimum rtt in ms
    max_rtt = max(rtt_times) * 1000  # maximum rtt in ms
    avg_rtt = statistics.mean(rtt_times) * 1000  # average rtt in ms
else:
    min_rtt = max_rtt = avg_rtt = 0
```

## Error Handling

The client handles the following types of errors:

**Timeout**
If no data was received within the timeout period, return timeout message
```python
whatReady = select.select([mySocket], [], [], timeLeft)
if whatReady[0] == []:
            return None, "Request timed out."
```
**ICMP Errors**
If a packet is lost, the client attempts to capture ICMP error messages. These errors indicate network issues, such as unreachable destinations, unreachable port, unreachable network

## Notes
-The client script requires elevated privileges to capture ICMP error messages using raw sockets (e.g., using sudo on Linux).
-This project simulates packet loss for testing purposes.
-Extract the value of icmp header, icmp type, icmp code correctly

## Troubleshooting

- **Timeouts**: If you experience high packet loss or timeouts, check the server's network and response handling.
- **Socket Errors**: Ensure that the server's ip address or domain name is correctly passed in the function

## Contact

For questions or contributions, please contact:

(mailto:cs24mtech14004@iith.ac.in)-- Ankush Chhabra <CS24MTECH14004 >
(mailto:sm24mtech11008@iith.ac.in)-- Rishabh Chaturvedi <SM24MTECH11008>
(mailto:cs24mtech11014@iith.ac.in)-- Jayanth Jatavath <CS24MTECH11014> 
