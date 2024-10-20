#Variables

#W=number of times a particular question is answered incorrectly
#Wc=number of times a particular question is answered correctly
#Wp=penalty for answering a question after it had been answered wrongly atleast once before

#D=Difficulty. Easy=1, Med=2, Hard=3
#PrS=Previous Score, always 0 while starting a test
#C=Correctness, +1 for correct, -1 for incorrect
#T=Time required to answer a question
#B=Bonus points for quick answer
#P=Penalty for slow answer

#Each Penalty or Bonus is a percent of PrS

def calc_score(PrS,D,C,B,P,W,Wc,CF,PR):
    if W==0:
        Wp=0
    else:
        if Wc==0:
            Wp = W*PR
        else:
            Wp= ((W-Wc)*CF)*PR
    score = (PrS+D*C)*(1+B-P-Wp)
    
    return score