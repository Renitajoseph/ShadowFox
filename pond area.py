radius = 84
pi = 3.14

# Calculate pond area
pond_area = pi * radius ** 2

# Calculate total water (liters) and convert to integer
water_per_sqm = 1.4
total_water = int(pond_area * water_per_sqm)

print("Total water in the pond:", total_water, "liters")