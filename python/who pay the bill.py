import random as rn
print ("whos pay the bill ?")
names= input("input names please ...")
sep = names.split(",") # مرج به لیست
print(sep)
count = len(sep)
#print(count)
chose = rn.randint (1,count)
#print(chose)
print(f"{sep[chose-1]} must pay the bill")