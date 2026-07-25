print ("welcome to the love calculator ... ")
name1=input("whats your name ? ")
name2=input("whats their name ? ")
uninameA = name1 + name2
uniname = uninameA.lower()
countt=uniname.count("t")
countr=uniname.count("r")
countu=uniname.count("u")
counte=uniname.count("e")
rate1=str(countt+countr+countu+counte)
countl=uniname.count("l")
counto=uniname.count("o")
countv=uniname.count("v")
counte=uniname.count("e")
rate2=str(countl+counto+countv+counte)
final = int(rate1+rate2)
print(final)
if final < 10 or final > 90 :
    print(f"your love score is {final} and you go together lik coke and mentos")
elif final >=40 and final <=50 :
    print (f"your love score is {final} and you are alright together")   
else :
    print(f"your love score is {final}")