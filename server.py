import socket
import random
from protocol import parse_packet, create_ack
from utils import calculate_hash

CHUNK_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5000))

print("Server listening...")

received_chunks = {}
expected_hash = None

while True:
    data, addr = sock.recvfrom(4096)

    # STEP 1: Client initiates connection
    if data == b"START":
        last_seq = max(received_chunks.keys()) if received_chunks else -1
        sock.sendto(f"RESUME {last_seq}".encode(), addr)
        print(f"Resume from {last_seq}")
        continue

    # STEP 2: Receive hash
    if data.startswith(b"HASH"):
        expected_hash = data.decode().split()[1]
        print("Expected hash:", expected_hash)
        continue

    # STEP 3: End signal
    if data == b"END":
        print("Rebuilding file...")

        with open("received_file.txt", "wb") as f:
            for i in sorted(received_chunks.keys()):
                f.write(received_chunks[i])

        actual_hash = calculate_hash("received_file.txt")

        if actual_hash == expected_hash:
            print("File OK")
        else:
            print("File corrupted")

        break

    # PACKET LOSS SIMULATION 
    # simulate 20% packet loss
    if random.random() < 0.2:
        print("Packet dropped!")
        continue

    # STEP 4: Receive chunk
    seq, chunk = parse_packet(data)

    # Avoid duplicate overwrite
    if seq not in received_chunks:
        received_chunks[seq] = chunk

    print(f"Received chunk {seq}")

    # Send ACK
    sock.sendto(create_ack(seq), addr)