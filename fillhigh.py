import cPickle
from classes import *

h1 = Score("Jack", 100)
h2 = Score("Jane", 200)
h3 = Score("John", 300)
h4 = Score("Jill", 400)
h5 = Score("Jonah", 500)
h6 = Score("Jenny", 600)
h7 = Score("Jeremiah", 700)
h8 = Score("Joanna", 800)
h9 = Score("Justin", 900)
h10 = Score("Judith", 1000)

hs = []
hs.append(h1)
hs.append(h2)
hs.append(h3)
hs.append(h4)
hs.append(h5)
hs.append(h6)
hs.append(h7)
hs.append(h8)
hs.append(h9)
hs.append(h10)

hs.sort(key=lambda x: x.score, reverse=True)
cPickle.dump(hs, file("highscore.dat", "wb"))
newhs = cPickle.load(file("highscore.dat", "rb"))

for score in newhs:
    print score.name+": "+str(score.score)+" - "+str(score.date)
