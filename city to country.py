# Define country-city mappings
countries = {
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth"],
    "UAE": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"],
    "India": ["Mumbai", "Bangalore", "Chennai", "Delhi"]
}

# Get user input
city = input("Enter a city name: ")

# Find matching country
for country, cities in countries.items():
    if city in cities:
        print(f"{city} is in {country}")
        break
else:  # No break (city not found)
    print(f"{city} is not in our database")