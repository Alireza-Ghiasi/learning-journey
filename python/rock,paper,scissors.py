import random as rn
choices = ['''   
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)

'''
,
'''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)

'''
,
'''
    _______
---'   ____)____
          ______)
         __________)
          (____)
---.__(___)

''']

user = int(input("enter 0 for rock, 1 for paper, 2 for scissors ..."))
airn = rn.randint(0,2)
if user not in [0, 1, 2]:
    print("invalid choice!")
    exit()
if user == airn :
    print (f"computer chose {choices[airn]} \n you chose {choices[user]}\n ... draw!!!!") 
elif (user == 0 and airn ==2) or (user == 1 and airn == 0) or (user == 2 and airn == 1) : 
    print (f"computer chose {choices[airn]} \n you chose {choices[user]}\n ... you win !") 
else :
    print (f"computer chose {choices[airn]} \n you chose {choices[user]}\n ... you lose !") 

