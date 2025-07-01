import random

# Initialize counters
count_6 = 0
count_1 = 0
consecutive_6 = 0
previous_roll = None

# Simulate 20 dice rolls
for _ in range(20):
    roll = random.randint(1, 6)
    print(f"Rolled: {roll}")
    
    # Count 6s and 1s
    if roll == 6:
        count_6 += 1
    elif roll == 1:
        count_1 += 1
    
    # Check for consecutive 6s
    if roll == 6 and previous_roll == 6:
        consecutive_6 += 1
    
    previous_roll = roll

# Print statistics
print("\nRoll Statistics:")
print(f"Number of 6s rolled: {count_6}")
print(f"Number of 1s rolled: {count_1}")
print(f"Number of two 6s in a row: {consecutive_6}")