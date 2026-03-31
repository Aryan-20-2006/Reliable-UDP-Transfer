import socket
import time
from protocol import create_packet, parse_ack
from utils import calculate_hash

SERVER_ADDR = ("127.0.0.1", 5000)
CHUNK_SIZE = 1024
TIMEOUT = 1
WINDOW_SIZE = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

filename = "file.txt"

#METRICS
start_time = None
end_time = None

total_bytes_sent = 0
total_packets_sent = 0
retransmissions = 0
acks_received = 0

send_times = {}
#

# STEP 1: Start + timing
start_time = time.time()
sock.sendto(b"START", SERVER_ADDR)

data, _ = sock.recvfrom(1024)
msg = data.decode()

if msg.startswith("RESUME"):
    resume_seq = int(msg.split()[1])
else:
    resume_seq = -1

print(f"Resuming from chunk {resume_seq}")

# STEP 2: Send hash
file_hash = calculate_hash(filename)
sock.sendto(f"HASH {file_hash}".encode(), SERVER_ADDR)

# STEP 3: Load file into chunks
packets = []

with open(filename, "rb") as f:
    f.seek((resume_seq + 1) * CHUNK_SIZE)
    seq = resume_seq + 1

    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        packets.append((seq, create_packet(seq, chunk)))
        seq += 1

total_packets = len(packets)

# STEP 4: Sliding window
base = 0
acked = set()

while base < total_packets:

    # Send window
    for i in range(base, min(base + WINDOW_SIZE, total_packets)):
        seq, packet = packets[i]

        sock.sendto(packet, SERVER_ADDR)

        total_packets_sent += 1
        total_bytes_sent += len(packet)

        send_times[seq] = time.time()

    try:
        while True:
            ack_data, _ = sock.recvfrom(1024)
            ack_seq = parse_ack(ack_data)

            if ack_seq is not None:
                acked.add(ack_seq)
                acks_received += 1

                # latency calculation
                if ack_seq in send_times:
                    latency = time.time() - send_times[ack_seq]
                    print(f"Latency for packet {ack_seq}: {latency:.4f} sec")

    except socket.timeout:
        retransmissions += WINDOW_SIZE  # approx

    # Slide window
    while base < total_packets and packets[base][0] in acked:
        print(f"ACK received for {packets[base][0]}")
        base += 1

# STEP 5: End transfer
sock.sendto(b"END", SERVER_ADDR)
end_time = time.time()

#METRICS OUTPUT
total_time = end_time - start_time

throughput = total_bytes_sent / total_time if total_time > 0 else 0
loss_rate = retransmissions / total_packets_sent if total_packets_sent > 0 else 0
efficiency = (total_packets_sent - retransmissions) / total_packets_sent if total_packets_sent > 0 else 0

print("\n--- Performance Metrics ---")
print(f"Time Taken: {total_time:.4f} sec")
print(f"Throughput: {throughput:.2f} bytes/sec")
print(f"Total Packets Sent: {total_packets_sent}")
print(f"Retransmissions: {retransmissions}")
print(f"Packet Loss Rate: {loss_rate:.4f}")
print(f"Efficiency: {efficiency:.4f}")
print(f"ACKs Received: {acks_received}")