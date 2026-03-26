# Reliable UDP File Transfer

Reliable file transfer over UDP using chunking, ACKs, resume support, and SHA256 validation.

## Table of Contents
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Files](#files)

## Quick Start
```bash
python server.py
python client.py
```

## How It Works
1. Client sends START and receives last confirmed chunk.
2. Client sends file hash, then chunked packets with sequence numbers.
3. Server ACKs received chunks and rebuilds the file on END.
4. Server verifies SHA256 hash to confirm integrity.

## Files
- client.py: Sender logic with sliding window.
- server.py: Receiver logic with ACK and file reconstruction.
- protocol.py: Packet and ACK encoding helpers.
- utils.py: SHA256 hash helper.
- file.txt: Sample input file.


