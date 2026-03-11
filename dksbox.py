import hashlib
import random

# 1. Dynamic Key Generation

def generate_dynamic_key(base_key: bytes, nonce: bytes, round_num: int) -> bytes:
    """
    Generate a new key for each round using hash-based derivation.
    base_key:  main secret key (e.g., 16 bytes)
    nonce:     unique value for each encryption
    round_num: current round number
    """
    data = base_key + nonce + round_num.to_bytes(2, 'big')
    dynamic_key = hashlib.sha256(data).digest()[:len(base_key)]  
    return dynamic_key


# 2. Dynamic S-Box Generation

def generate_dynamic_sbox(dynamic_key: bytes):
    """
    Create a simple dynamic S-box based on key-derived randomness.
    """
    seed = int.from_bytes(hashlib.sha256(dynamic_key).digest(), 'big')
    random.seed(seed)
    sbox = list(range(256))  
    random.shuffle(sbox)
    return sbox

# 3. Example Demonstration

base_key = b"mysecretkey12345"   
nonce = b"unique_nonce"          
total_rounds = 5
for r in range(total_rounds):
    dyn_key = generate_dynamic_key(base_key, nonce, r)
    dyn_sbox = generate_dynamic_sbox(dyn_key)
    print(f"\n🔹 Round {r+1}")
    print(f"Dynamic Key: {dyn_key.hex()}")
    print(f"S-Box (first 16 entries): {dyn_sbox[:16]}")
