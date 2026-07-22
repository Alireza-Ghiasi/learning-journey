print ("welcome to the tip calculator")
total=float(input("what was total bill ? "))
tip=int(input("what percent tip would you like to pay ,10,12,15,... ? "))
num=int(input("how many people to split the bill ? "))
finalbill = total * (tip/100) + total
eachperson = round(finalbill/num ,2)
print(f"your final bill = {finalbill} ")
print(f"each person shuld pay : {eachperson}")