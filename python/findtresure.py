import random as rn
row1 = ["y","y","y"]
row2 = ["y","y","y"]
row3 = ["y","y","y"]
map = [row1,row2,row3]
horizonal = rn.randint(1,3) #soton
vertical = rn.randint(1,3) #satr
map[vertical -1][horizonal-1] = "x"
#print(f"{row1}\n{row2}\n{row3}")

chance = 3

while chance > 0:

    guss = input("Where is the treasure? horizontal and vertical: ")

    hor = int(guss[0])
    ver = int(guss[1])

    if map[ver - 1][hor - 1] == "x":
        print("Congratulations!!!! You found the treasure!")
        break

    else:
        chance -= 1
        print("Sorry! Wrong guess.")

        print(f"You have {chance} chances left.")

if chance == 0:
    print("You lose!")
    print(f"{row1}\n{row2}\n{row3}")

