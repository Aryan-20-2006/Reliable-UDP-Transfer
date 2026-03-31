#Uses hashing and helper functions

import hashlib

def calculate_hash(filename):
    sha256=hashlib.sha256()
    
    with open(filename,"rb") as f:
        while chunk :=f.read(4096):
                sha256.update(chunk)
                
    return sha256.hexdigest()
