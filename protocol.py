def create_packet(seq,data):
        return seq.to_bytes(4,'big')+data

def parse_packet(packet):
    seq=int.from_bytes(packet[:4],'big')
    data=packet[4:]
    return seq,data

def create_ack(seq):
    return f"ACK {seq}".encode()

def parse_ack(data):
    try:
        msg=data.decode()
        if msg.startswith("ACK"):
            return int(msg.split()[1])
    except:
        pass
    return None   
    