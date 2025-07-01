distance = 490  # meters
time_minutes = 7

# Convert time to seconds
time_seconds = time_minutes * 60

# Calculate speed (m/s) and convert to integer
speed = int(distance / time_seconds)

print("Speed:", speed, "m/s")