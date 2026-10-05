row1 = ["y","y","y"]
row2 = ["y","y","y"]
row3 = ["y","y","y"]
map = [row1,row2,row3]
print(f"{row1}\n{row2}\n{row3}")
postion = input("which horizonal and vertical ?enter by order?")
horizonal = int(postion[0])
vertical = int(postion[1])
map[vertical -1][horizonal-1] = "x"
print(f"{row1}\n{row2}\n{row3}")
