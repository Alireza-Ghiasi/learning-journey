stdscore = input("enter the score of student").split()
for h in stdscore :
    if not h.isdigit():
        print("invalid input")
        exit()
if len(stdscore) == 0:
    print("No scores entered")
    exit()        
snum = 0        
for m in stdscore:
    snum += 1
print (f"number of students is {snum}")             
for i in range (0,snum) :   
    stdscore[i]= int (stdscore[i])    
print (f"th list of scores ... {stdscore} ")     
maxi = stdscore [0]
for x in stdscore:
    if x>maxi :
        maxi = x
stdsum = 0        
print(f"the maximum score is {maxi}")      
for i in stdscore :
    stdsum += i
print(f"sum of scores is {stdsum}")
mini = stdscore [0]
for w in stdscore:
    if w < mini :
        mini = w
print(f"minimum of score is {mini}")
print (f"average of class score is {round(stdsum/snum,3)}")