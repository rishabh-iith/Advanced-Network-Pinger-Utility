# Advanced-Network-Pinger-Utility
Socket Programming (UDP, TCP, ICMP), Multi-threading, Raw Sockets, Packet Loss Simulation (tc-netem), Error Handling

## Table of Contents

- [Overview](#overview)
- [ICMP Ping Program](#icmp-ping-program)
- [TCP Ping Program](#tcp-ping-program)
- [UDP Ping Program](#udp-ping-program)
- [General Requirements](#general-requirements)
- [Setup and Usage](#setup-and-usage)
- [Error Handling](#error-handling)
- [Notes](#notes)
- [Troubleshooting](#troubleshooting)
- [Contact](#contact)

## Overview

This project includes implementations of server-client ping programs using ICMP, TCP, and UDP protocols. Each program measures round-trip time (RTT), calculates statistics, and simulates packet loss where applicable. The ICMP program uses Python’s raw sockets, while the TCP and UDP implementations utilize Python's `socket` library.

---

## ICMP Ping Program

### Features:

- Sends ICMP Echo Requests and receives Echo Replies.
- Measures RTT for each successful ping.
- Calculates and displays minimum, maximum, and average RTT along with packet loss rate.
- Captures ICMP error messages.

### Setup and Usage:

1. Save the client code as `client.py`.
2. Run the client to send ping requests to a specified server (e.g., `google.com`).

```bash
sudo python3 client.py
```

---

## TCP Ping Program

### Features:

- **Server**:
  - Listens for incoming TCP connections.
  - Handles multiple clients using multithreading.
  - Simulates 20% packet loss.
- **Client**:
  - Sends a specified number of ping requests to the server.
  - Measures RTT and calculates statistics.
  - Handles ICMP error messages for timeouts.

### Setup and Usage:

1. Save the server code as `tcp_server.py` and the client code as `tcp_client.py`.
2. Start the server:

```bash
python3 tcp_server.py
```

3. Run the client:

```bash
sudo python3 tcp_client.py
```

---

## UDP Ping Program

### Features:

- **Server**:
  - Listens for UDP packets.
  - Simulates 20% packet loss.
  - Responds to clients by capitalizing received messages.
- **Client**:
  - Sends UDP ping requests to the server.
  - Measures RTT and calculates statistics.
  - Captures ICMP error messages for timeouts.

### Setup and Usage:

1. Save the server code as `server.py` and the client code as `client.py`.
2. Start the server:

```bash
python3 server.py
```

3. Run the client:

```bash
sudo python3 client.py
```

---

## General Requirements

- Python 3.x
- Elevated privileges (e.g., `sudo`) may be required for ICMP programs or to capture ICMP error messages in TCP and UDP.
- Basic understanding of networking and sockets.

---

## Error Handling

### ICMP Program:

- Handles timeouts by returning a "Request timed out" message.
- Captures ICMP error messages for issues like unreachable destinations.

### TCP and UDP Programs:

- **Timeouts**: Logs packet as lost if the server does not respond within 1 second.
- **ICMP Errors**: Attempts to capture error messages using raw sockets.

---

## Notes

- Ensure the server is running and reachable at the correct IP address and port for TCP and UDP programs.
- Simulated packet loss in TCP and UDP programs can be adjusted in the code.
- ICMP programs require raw sockets and may need administrative privileges.

---

## Troubleshooting

- **Timeouts**: Check network connectivity and ensure the server is correctly configured.
- **Socket Errors**: Verify the server’s IP address and port.
- **Packet Loss**: For UDP, use `tc netem` in Linux to emulate packet loss at the NIC level.

---
