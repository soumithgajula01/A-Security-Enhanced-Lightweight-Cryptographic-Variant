
ascon_time = 0.038995     
dascon_time = 0.424839     

ascon_throughput = 410309.013977    
dascon_throughput = 37661.303658    

ascon_freq = 0.025644      
dascon_freq = 0.002354     

# %change = ((new - old) / old) * 100


def percentage_change(old, new):
    return ((new - old) / old) * 100



exec_time_change = percentage_change(ascon_time, dascon_time)
throughput_change = percentage_change(ascon_throughput, dascon_throughput)
frequency_change = percentage_change(ascon_freq, dascon_freq)


print("=== Percentage Change (ASCON → DASCON) ===\n")

print(f"Execution Time Increase: {exec_time_change:.2f}%")
print(f"Throughput Change: {throughput_change:.2f}%")
print(f"Frequency Change: {frequency_change:.2f}%")

print("\nNOTE: Positive = Increase, Negative = Decrease\n")
