# Reliable UDP File Transfer System

A reliable and resumable file transfer system built over UDP using custom protocol mechanisms.

---

## Features

- Chunk-based file transfer
- Resume interrupted transfers
- Acknowledgment-based reliability (ACKs)
- Sliding window for throughput optimization
- File integrity verification using SHA-256 hashing
- Performance metrics analysis
- Packet loss simulation for testing robustness

---

## System Overview

This system implements a reliable data transfer protocol over UDP by incorporating mechanisms similar to transport layer protocols.

The workflow is as follows:

1. The client initiates communication using a `START` message.
2. The server responds with the last successfully received chunk.
3. The client resumes transmission from that point.
4. File data is divided into fixed-size chunks with sequence numbers.
5. Each chunk is sent and acknowledged by the server.
6. A sliding window mechanism is used to improve throughput.
7. After all chunks are received, the server reconstructs the file.
8. A SHA-256 hash is used to verify file integrity.

---

## Setup Instructions

### Prerequisites

- Python 3.x installed on your system

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <repository-folder>

### Usage Instructions

Step 1:Start the Server

python server.py

Step 2:Run the Client

python client.py

