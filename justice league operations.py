# Initial Justice League list
justice_league = ["Superman", "Batman", "Wonder Woman", "Flash", "Aquaman", "Green Lantern"]
print("Step 0 - Initial list:", justice_league)

# 1. Calculate number of members
num_members = len(justice_league)
print(f"Step 1 - Number of members: {num_members}")

# 2. Add Batgirl and Nightwing
justice_league.extend(["Batgirl", "Nightwing"])
print("Step 2 - After adding Batgirl and Nightwing:", justice_league)

# 3. Move Wonder Woman to front
justice_league.remove("Wonder Woman")
justice_league.insert(0, "Wonder Woman")
print("Step 3 - Wonder Woman moved to front:", justice_league)

# 4. Separate Aquaman and Flash using Green Lantern
# Find current positions
flash_index = justice_league.index("Flash")
aquaman_index = justice_league.index("Aquaman")

# Determine who to move (choose Green Lantern)
justice_league.remove("Green Lantern")
# Insert after Flash (who comes before Aquaman in current order)
justice_league.insert(flash_index + 1, "Green Lantern")
print("Step 4 - Green Lantern moved between Flash and Aquaman:", justice_league)

# 5. Replace entire team with new members
justice_league = ["Cyborg", "Shazam", "Hawkgirl", "Martian Manhunter", "Green Arrow"]
print("Step 5 - New team after crisis:", justice_league)

# 6. Sort alphabetically and identify new leader
justice_league.sort()
print("Step 6 - Sorted Justice League:", justice_league)
print(f"BONUS: The new leader is '{justice_league[0]}'")