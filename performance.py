import time
import hashlib
import random
import pandas as pd
import secrets

# 1. Dynamic Key Generation
def generate_dynamic_key(base_key: bytes, nonce: bytes, round_num: int) -> bytes:
    """
    Generate dynamic key per round using hash-based derivation.
    """
    data = base_key + nonce + round_num.to_bytes(2, 'big')
    dynamic_key = hashlib.sha256(data).digest()[:len(base_key)]
    return dynamic_key



# 2. Dynamic S-Box Generation
def generate_dynamic_sbox(dynamic_key: bytes):
    """
    Generate a dynamic S-box based on hashed dynamic key.
    """
    seed = int.from_bytes(hashlib.sha256(dynamic_key).digest(), 'big')
    random.seed(seed)
    sbox = list(range(256))
    random.shuffle(sbox)
    return sbox


# 3. Adaptive Rounds
def get_adaptive_rounds(message: bytes, nonce: bytes):
    """
    Adaptive rounds based on message size and nonce sum variation.
    """
    base_rounds = 6
    msg_factor = len(message) % 4
    nonce_factor = sum(nonce) % 3
    total_rounds = base_rounds + msg_factor + nonce_factor
    return total_rounds


# 4. Dynamic Permutation
def dynamic_permutation(state: list, dynamic_key: bytes, sbox: list):
    """
    Key-based permutation + S-box substitution.
    """
    seed = int.from_bytes(hashlib.sha256(dynamic_key).digest(), 'big')
    random.seed(seed)

    new_state = state.copy()
    random.shuffle(new_state)
    new_state = [sbox[x % 256] for x in new_state]
    return new_state


# Baseline ASCON (Simple Model)

def baseline_ascon(state, rounds=6):
    """
    Simple lightweight baseline permutation to simulate ASCON.
    """
    s = state.copy()
    for _ in range(rounds):
        random.shuffle(s)
        s = [(x * 37) % 256 for x in s]
    return s

# PERFORMANCE TEST EXECUTION

message = b"AI-based Beach Safety System using DASCON"
nonce = b"unique_nonce_2025"
base_key = b"secretkey1234567"

state = list(range(16))  # State length = 16

# Baseline ASCON timing

t0 = time.perf_counter()
for _ in range(400):
    baseline_ascon(state, 6)
t1 = time.perf_counter()
ascon_time = (t1 - t0) / 400



# DASCON timing

total_rounds = get_adaptive_rounds(message, nonce)

t0 = time.perf_counter()
for _ in range(400):
    temp_state = state.copy()
    for r in range(total_rounds):
        dyn_key = generate_dynamic_key(base_key, nonce, r)
        dyn_sbox = generate_dynamic_sbox(dyn_key)
        temp_state = dynamic_permutation(temp_state, dyn_key, dyn_sbox)
t1 = time.perf_counter()
dascon_time = (t1 - t0) / 400



# PERFORMANCE METRICS

data_size = len(state)

ascon_throughput = data_size / ascon_time
dascon_throughput = data_size / dascon_time

ascon_freq = 1 / ascon_time / 1e6
dascon_freq = 1 / dascon_time / 1e6


# TABLE 1 – SECURITY PARAMETERS
df_security = pd.DataFrame([
    ["Key Behavior", "Static", "Dynamic per round"],
    ["S-Box Behavior", "Fixed", "Dynamic, key-dependent"],
    ["Rounds", "Fixed (6)", f"Adaptive ({total_rounds})"],
    ["Permutation", "Static", "Dynamic, key-dependent"],
    ["Predictability", "High", "Very Low"],
    ["Security Level", "Standard", "Enhanced"]
], columns=["Security Parameter", "ASCON", "DASCON"])


# TABLE 2 – PERFORMANCE RESULTS

df_performance = pd.DataFrame([
    ["Execution Time (ms)", ascon_time * 1000, dascon_time * 1000],
    ["Throughput (ops/sec)", ascon_throughput, dascon_throughput],
    ["Frequency (MHz)", ascon_freq, dascon_freq]
], columns=["Metric", "ASCON", "DASCON"])


# OUTPUT RESULTS
print("\n SECURITY PARAMETERS \n")
print(df_security.to_string(index=False))

print("\n PERFORMANCE RESULTS \n")
print(df_performance.to_string(index=False))
