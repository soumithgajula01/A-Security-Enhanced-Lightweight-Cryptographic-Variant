import hashlib
import random

# 1. Dynamic Key Generation

def generate_dynamic_key(base_key: bytes, nonce: bytes, round_num: int) -> bytes:
    """
    Generate a round-specific dynamic key using hash-based derivation.
    """
    data = base_key + nonce + round_num.to_bytes(2, 'big')
    dynamic_key = hashlib.sha256(data).digest()[:len(base_key)]
    return dynamic_key

# 2. Dynamic S-Box Generation

def generate_dynamic_sbox(dynamic_key: bytes):
    """
    Generate a key-dependent dynamic S-box for each round.
    """
    seed = int.from_bytes(hashlib.sha256(dynamic_key).digest(), 'big')
    random.seed(seed)
    sbox = list(range(256))
    random.shuffle(sbox)
    return sbox


# 3. Adaptive Round Control

def get_adaptive_rounds(message: bytes, nonce: bytes):
    """
    Dynamically set total encryption rounds based on message length and nonce.
    """
    base_rounds = 6
    msg_factor = len(message) % 4
    nonce_factor = sum(nonce) % 3
    total_rounds = base_rounds + msg_factor + nonce_factor
    return total_rounds


# 4. Dynamic Internal Permutation (key-dependent)

def dynamic_permutation(state: list, dynamic_key: bytes, sbox: list):
    """
    Perform a key-dependent permutation on the internal state:
    - Shuffle state based on key randomness
    - Substitute values using dynamic S-box
    """
    seed = int.from_bytes(hashlib.sha256(dynamic_key).digest(), 'big')
    random.seed(seed)

    new_state = state.copy()
    random.shuffle(new_state)

    new_state = [sbox[x % 256] for x in new_state]
    return new_state


# 5. Main DASCON Demonstration


message = b"AI-based Beach Safety System using DASCON"
nonce = b"unique_nonce_2025"
base_key = b"secretkey1234567" 
total_rounds = get_adaptive_rounds(message, nonce)
print(f"🔹 Total Adaptive Rounds: {total_rounds}")
state = list(range(16))
for r in range(total_rounds):
    dyn_key = generate_dynamic_key(base_key, nonce, r)
    dyn_sbox = generate_dynamic_sbox(dyn_key)
    state = dynamic_permutation(state, dyn_key, dyn_sbox)
    print(f"\n Round {r+1}")
    print(f"Dynamic Key: {dyn_key.hex()[:32]}...")
    print(f"S-Box (first 10): {dyn_sbox[:10]}")
    print(f"State (first 8): {state[:8]} ...")
