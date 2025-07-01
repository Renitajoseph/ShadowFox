total_jacks = 0
sets_completed = 0

for set_num in range(10):
    # Perform a set
    print(f"\nPerforming set {set_num + 1} - 10 jumping jacks")
    total_jacks += 10
    sets_completed += 1
    
    # Check if all sets are completed
    if sets_completed == 10:
        print("Congratulations! You completed the workout")
        break
        
    # Ask about tiredness
    tired = input("Are you tired? (yes/y or no/n): ").strip().lower()
    
    if tired in ['yes', 'y']:
        skip = input("Do you want to skip the remaining sets? (yes/y or no/n): ").strip().lower()
        if skip in ['yes', 'y']:
            print(f"You completed a total of {total_jacks} jumping jacks")
            break
        else:
            remaining = 100 - total_jacks
            print(f"Continue! {remaining} jumping jacks remaining")
    else:
        remaining = 100 - total_jacks
        print(f"Great! {remaining} jumping jacks remaining")