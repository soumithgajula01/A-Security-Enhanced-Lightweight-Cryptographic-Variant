import hashlib
import random

# 1. Adaptive Round Controller

def get_adaptive_rounds(message: bytes, nonce: bytes):
    """
    Dynamically determine the number of rounds based on:
    - message length
    - nonce randomness
    """
    base_rounds = 6
    msg_factor = len(message) % 4  
    nonce_factor = sum(nonce) % 3  
    total_rounds = base_rounds + msg_factor + nonce_factor
    return total_rounds



# 2. Dynamic Permutation Function

def dynamic_permutation(state: list, round_key: bytes):
    """
    Perform a simple round permutation using key-derived randomness.
    """
    seed = int.from_bytes(hashlib.sha256(round_key).digest(), 'big')
    random.seed(seed)

    new_state = state.copy()
    random.shuffle(new_state)
    return new_state


# 3. Example Demonstration

message = b"AI-based Beach Safety System"
nonce = b"unique_nonce_2025"
base_key = b"secretkey1234567"
rounds = get_adaptive_rounds(message, nonce)
print(f"🔹 Adaptive Rounds Selected: {rounds}")
state = list(range(16))  
for r in range(rounds):
    round_key = hashlib.sha256(base_key + r.to_bytes(2, 'big')).digest()[:16]
    state = dynamic_permutation(state, round_key)
    print(f"Round {r+1}: State -> {state[:8]} ...")  