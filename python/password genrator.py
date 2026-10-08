import random as rn

alpha = "abcdefghijklmnopqrstuvwxyz"
number = "0123456789"
symbol = "!@#$%&*"
password = ""
passx = ""
numberofalpha = int(input("how many letters? "))
numberofnum = int(input("how many numbers? "))
numberofsym = int(input("how many symbol? "))

numbofchar = numberofsym + numberofnum + numberofalpha

while numberofalpha > 0:
    letter = rn.randint(0, 25)
    password += alpha[letter]
    numberofalpha -= 1

while numberofnum > 0:
    num = rn.randint(0, 9)
    password += number[num]
    numberofnum -= 1

while numberofsym  > 0:
    sym = rn.randint(0, 5)
    password += symbol[sym]
    numberofsym -= 1        

passx = list(password)

rn.shuffle(passx)

passx = "".join(passx)

print(passx)