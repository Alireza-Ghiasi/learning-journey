a=float(input("whats yor weghit in kg ?"))
b=float(input("whats your hight in m ?"))
bmi = a / (b**2)
print ("your bmi is" , bmi)
if bmi < 18.5:
    print("Underweight")
elif bmi < 25:
    print("Normal weight")
elif bmi < 30:
    print("Overweight")
elif bmi < 35:
    print("Obesity Class I")
elif bmi < 40:
    print("Obesity Class II")
else:
    print("Obesity Class III")