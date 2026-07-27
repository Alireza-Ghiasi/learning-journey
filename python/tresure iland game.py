print('''*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."'` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/______/_
*******************************************************************************''')
print("wellcome to the tresure island ... \nyour mission is to find the tresure")
dec1=input("youre at a cross road ... wehere do you whant to go ? left or right ?")
if dec1 == "left" :
    dec2=input("you come to a lake.there is an island in the middle of the lake\n type 'wait' for wait for a boat or 'swim' to swim across")
    if dec2=="wait":
        dec3=input("you arrive at the island unharmed. there is a house with 3 doors red blue and yellow which colour do you chose ?")
        if dec3 == "yellow" :
            print("you find the treasure ,you win !!!")
        elif dec3 == "blue" :
            print("you chose beast house , you lose !")   
        elif dec3 == "red":
            print("you chose fire house , you lose !")    
        else :
            print("uncertain world,you lose. try again")    
    elif dec2 == "swim" :
        print ("you have eaten by lake monster , you lose!")
    else :
        print ("uncertain world, you lose. try again")     
elif dec1 == "right" :
    print ("you have lost ! you lose !")
else :
    print ("uncertain world,you lose. try again")    