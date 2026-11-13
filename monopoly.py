from fractions import Fraction
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd

### This file is used to construct the markox matrix A from its parts
### and is used to find the eigenvalues and eigenvectors and the steady
### state probability distribution vector pi.

dice = [1.0/36.0, 1.0/18.0, 1.0/12.0, 1.0/9.0, 5.0/36.0, 1.0/6.0, 5.0/36.0, 1.0/9.0, 1.0/12.0, 1.0/18.0, 1.0/36.0]
chance = [7, 22, 36]
dest = np.array([0, 24, 39, 11, 40, 5])
community_chest = [2, 17, 33]
stations = [5, 15, 25, 35]
utility = [12, 28]

cols = 43
rows = 43

M = np.zeros((rows, cols), dtype=float)

D = np.zeros((rows, cols), dtype=float)

J = np.zeros((rows, cols), dtype=float)

F = np.zeros((rows, cols), dtype=float)
F[40,: ] = 1/216

R = np.eye(cols)

def apply_cards(M):

    for i in community_chest:
    ### 2, 17 and 33 are the CCs
    ### 14/16 cards let them stay. 1 card sends them to Go. 1 card to jail yikes
    ### essentially, the final position of someone who lands on a community chest is 14/16*A[community chest][col]
    ### A[0][col] = 1/16, A[40][col] = 1/16

        M[0,:] = M[0,:] + 1/16*M[i,:]
        M[40,:] = M[40,:] + 1/16*M[i,:]
        M[i,:] *= 14/16


    for i in chance:

    ### 6/16 chance of staying. 10/16 of leaving
    ### 5 tiles to go to. 1 jail, back 3 spaces
    ### 2 nearest stations, 1 nearest utility

        chancerow = M[i,:].copy()
        for j in dest:
            M[j,:] += chancerow * 1/16

        if i != 36:
            M[i-3,:] += chancerow * 1/16

        ### special case for i = 36 since 3 spaces back is a CC card
        elif i == 36:
            ### 1/16 chance of going back 3 steps
            ### 14/16 chance of staying there
            ### so 14/256 going back 3 steps and staying
            M[33,:] += M[36,:] * 1.0/16.0 * 14.0/16.0
            M[0,:] += M[36,:] * 1.0/16.0 * 1.0/16.0
            M[40,:] += M[36,:] * 1.0/16.0 * 1.0/16.0

        ### nearest station
        nearest = False
        for j in stations:
            if j > i:
                ### find railroad with position greater than curr pos
                nearest = True
                M[j,:] += chancerow * 1/8
                break;
        ### need to pass go to reach a railroad
        if nearest == False:
            M[stations[0], :] += chancerow *1/8

        nearest = False 

        ### nearest utility
        for j in utility:
            if j > i:
                ### find utility with position greater than curr pos
                nearest=True
                M[j,:] += chancerow * 1.0/16.0
                break;
        ### need to pass go to reach a utility
        if nearest == False:
            M[utility[0], :] += chancerow *1/16.0

        M[i,:] *= 6/16
    
    return M


for i in range(cols):
### Handles case 1: players jail transition states
### The rules state that when you throw doubles to
### get out of jail, you advance by that number of
### squares, but you do not get another roll
### So this makes sense
    if i == 30:
        M[40, i] = 5.0/6.0
        D[40, i] = 1.0/6.0
    elif i == 40 or i == 41:
        for j in range(12, 23, 2):
            M[j, i] = 1.0/36.0
        M[i+1, i] = 5.0/6.0

    ### the rule state that on the third throw (jail state 3) if you don't roll a double
    ### you pay a fine and advance the number of squares you roll
    elif i == 42:
        for j in range(12, 23):
            M[j, i] = dice[j-12]
    else:
    ### Handles case 2: the normal case of rolling the dice
        starting_idx = (i+2)%40
        for counter in range(0, 11):
            if starting_idx == 30:
                M[40, i] = dice[counter]
                if (counter % 2 == 0):
                    M[40, i] -= 1/36
                    D[40, i] += 1/36
            else:
                M[starting_idx, i] = dice[counter]
                if counter % 2 == 0:
                    M[starting_idx, i] -= 1/36
                    D[starting_idx, i] += 1/36
            starting_idx += 1
            if starting_idx > 39:
                starting_idx %= 40   

M = apply_cards(M)
D = apply_cards(D)


### Transferring the jail transition states to a Jail matrix.
### The jail matrix handles the rolling doubles to get out of jail and advancing
### mechanism. The jail matrix also handles transitioning from jail state 1 to 2 to 3.

J[:, 40:] = M[:, 40:]
M[:, 40:] = 0
D[:, 40:] = 0

M[40, 40] = 5/6
D[40, 40] = 1/6


A = M + M @ D + M @ D @ D + F

A[:, 40:] = J[:, 40:]

# for j in range(cols):
#     s=0
#     for i in A[:,j]:
#         s+=i
#     print(s)


eigenvalues, eigenvectors = np.linalg.eig(A)

order = np.argsort(-np.abs(eigenvalues))

eigenvalues = eigenvalues[order]
eigenvectors = eigenvectors[:,order]


x = np.zeros(cols)
x[0] = 1

c = np.linalg.solve(eigenvectors, x)

pi = abs(c[0] * eigenvectors[:,0])

order = np.argsort(-pi)

with open(file = "tile names.txt", mode = "r") as f:
    square_names = [line.strip() for line in f if line.strip()]

# for idx in order[:20]:
#     print(f"{square_names[idx]:<28} {pi[idx]:.5f}")

# keep = [i for i in range(43) if i != 30]
# A_sub = A[np.ix_(keep, keep)]

# print(np.allclose(A_sub.sum(axis=0), 1))     # columns still sum to 1
# P = np.linalg.matrix_power(A_sub, 200)
# print((P > 0).all())          
# C=A@A
# print(C[:,0][9])