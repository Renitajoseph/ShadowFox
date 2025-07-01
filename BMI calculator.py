# Get user inputs
height = float(input("Enter height in meters: "))
weight = float(input("Enter weight in kilograms: "))

# Calculate BMI
bmi = weight / (height ** 2)

# Determine and print category
if bmi >= 30:
    print("Obesity")
elif bmi >= 25:  # 25 <= bmi < 30
    print("Overweight")
elif bmi >= 18.5:  # 18.5 <= bmi < 25
    print("Normal")
else:  # bmi < 18.5
    print("Underweight")