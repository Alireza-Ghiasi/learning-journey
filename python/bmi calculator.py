a=float(input("whats yor weghit in kg ?"))
b=float(input("whats your hight in m ?"))
bmi = round( a / (b**2),1)
min_weight = 18.5 * (b ** 2)
max_weight = 24.9 * (b ** 2)
print ("your bmi is" , bmi)
if bmi < 18.5:
    print(f"Underweight, A healthy weight range for you is {min_weight} to {max_weight} kg")
    need_gain = round(min_weight - a, 1)
    print(f"You need to gain about {need_gain} kg")
elif bmi < 25:
    print("Normal weight")
elif bmi < 30:
    print(f"Overweight, A healthy weight range for you is {min_weight} to {max_weight} kg")
    need_lose = round(a - max_weight, 1)
    print(f"You need to lose about {need_lose} kg")
elif bmi < 35:
    print(f"Obesity Class I A healthy weight range for you is {min_weight} to {max_weight} kg")
    need_lose = round(a - max_weight, 1)
    print(f"You need to lose about {need_lose} kg")
elif bmi < 40:
    print(f"Obesity Class II A healthy weight range for you is {min_weight} to {max_weight} kg")
    need_lose = round(a - max_weight, 1)
    print(f"You need to lose about {need_lose} kg")
else:
    print(f"Obesity Class III A healthy weight range for you is {min_weight} to {max_weight} kg")
    need_lose = round(a - max_weight, 1)
    print(f"You need to lose about {need_lose} kg")