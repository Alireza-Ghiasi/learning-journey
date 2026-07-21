num = int(input("whats the number ?"))
sum_num = 0
while num > 0 :
    sum_num += num% 10
    num //= 10
print("sum of numbers is :" , sum_num)    
print (type(num))