from markov_matrix import A, cols
from landing_matrix import L, v

import numpy as np


checkpoints = [25, 50, 100, 200, 500, 1000]

x = v

# print("Orange:")
# print("Turns to recoup:", 560/(14*x[16] + 14*x[18] + 16*x[19]))
# print("Probability:", x[16] + x[18] + x[19])
# print("Rent:", 44)
# print("EV:", 14*x[16] + 14*x[18] + 16*x[19], "\n")


# print("Red:")
# print("Turns to recoup:", 680/(18*x[21] + 18*x[23] + 20*x[24]))
# print("Probability:", x[21] + x[23] + x[24])
# print("Rent:", 18+18+20)
# print("EV:", 18*x[21] + 18*x[23] + 20*x[24], "\n")

# print("Purple:")
# print("Turns to recoup:", 750/(35*x[37] + 50*x[39]))
# print("Probability:", x[37] + x[39])
# print("Rent:", 85)
# print("EV:", 35*x[37] + 50*x[39])



print("Orange:")
print("Turns to recoup:", 860/(70*x[16] + 70*x[18] + 80*x[19]))
print("Probability:", x[16] + x[18] + x[19])
print("Rent:", 220)
print("EV:", 70*x[16] + 70*x[18] + 80*x[19], "\n")


print("Red:")
print("Turns to recoup:", 1130/(90*x[21] + 90*x[23] + 100*x[24]))
print("Probability:", x[21] + x[23] + x[24])
print("Rent:", 180+100)
print("EV:", 90*x[21] + 90*x[23] + 100*x[24], "\n")

print("Purple:")
print("Turns to recoup:", 1150/(175*x[37] + 200*x[39]))
print("Probability:", x[37] + x[39])
print("Rent:", 375)
print("EV:", 175*x[37] + 200*x[39])




