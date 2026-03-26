# client.py

import socket
from protocol import create_packet, parse_ack
from utils import calculate_hash

SERVER_ADDR = ("127.0.0.1", 5000)
CHUNK_SIZE = 1024
TIMEOUT = 1
WINDOW_SIZE = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

filename = "file.txt"

# STEP 1: Start + get resume info
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

# STEP 4: Sliding window send
base = 0
acked = set()

while base < total_packets:

    # Send window
    for i in range(base, min(base + WINDOW_SIZE, total_packets)):
        seq, packet = packets[i]
        sock.sendto(packet, SERVER_ADDR)

    try:
        while True:
            ack_data, _ = sock.recvfrom(1024)
            ack_seq = parse_ack(ack_data)

            if ack_seq is not None:
                acked.add(ack_seq)

    except socket.timeout:
        pass

    # Slide window
    while base < total_packets and packets[base][0] in acked:
        print(f"ACK received for {packets[base][0]}")
        base += 1

# STEP 5: End transfer
sock.sendto(b"END", SERVER_ADDR)

print("File sent successfully")