from monopoly import A, cols
from MC import markov_freq

import numpy as np


checkpoints = [25, 50, 100, 200, 500, 1000]

x = markov_freq(55)

print("Orange:")
print("Turns to recoup:", 680/(14*x[16] + 14*x[18] + 16*x[19]+ 200))
print("Probability:", x[16] + x[18] + x[19])
print("Rent:", 44)
print("EV:", 44*(x[16] + x[18] + x[19]), "\n")


print("Red:")
print("Turns to recoup:", 680/(18*x[21] + 18*x[23] + 20*x[24]+ 200))
print("Probability:", x[21] + x[23] + x[24])
print("Rent:", 18+18+20)
print("EV:", 56*(x[21] + x[23] + x[24]), "\n")

print("Purple:")
print("Turns to recoup:", 750/(35*x[37] + 50*x[39] + 200))
print("Probability:", x[37] + x[39])
print("Rent:", 85)
print("EV:", 85*(x[37] + x[39]))







