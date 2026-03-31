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

## How It Works

1. Client sends a `START` request to the server.
2. Server responds with the last received chunk (resume support).
3. Client sends file hash for integrity verification.
4. File is split into chunks and sent with sequence numbers.
5. Server acknowledges each chunk (ACKs).
6. Sliding window improves throughput by sending multiple packets.
7. On completion, server reconstructs the file.
8. Hash is verified to ensure file integrity.

---

## Performance Metrics

The system evaluates performance using the following metrics:

- Throughput  
  Measures how fast data is transferred (bytes/sec)

- Transfer Time  
  Total time taken for file transfer

- Retransmissions  
  Number of packets resent due to loss

- Packet Loss Rate  
  Ratio of retransmissions to total packets sent

- Efficiency  
  Ratio of successful transmissions to total transmissions

- Latency (per packet)  
  Time taken for a packet to receive acknowledgment

---

## Packet Loss Simulation

To simulate real-world network conditions, random packet loss is introduced at the server:

```python
if random.random() < 0.2:
    continue