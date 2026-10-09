
stdhight= input("enter student's hight in cm ...").split()
for h in stdhight :
    if not h.isdigit():
        print("invalid number")
        exit()
for n in range (0 , len(stdhight)) :
    stdhight[n] = int(stdhight[n])
print(stdhight)    
hightsum = 0
lengh=(len(stdhight))
#i=0
for i in stdhight :
    hightsum+=i

print (f"avrage of students hight is {round(hightsum/lengh,3)}")