from fractions import Fraction
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd



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
    ### 6 tiles to go to. 1 jail, back 3 spaces
    ### 2 nearest stations, 2 nearest utility

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
        D[40, i] = 1/0/6.0
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
M[40, 40] = 5/6
D[40, 40] = 1/6

for j in range(cols):
    s = 0;
    for i in M[:,j]:
        s+= i
    if abs(s-5/6) >= 1e-6:
        print(s)

print("above cols dont sum to")






# for i in chance:
#     R[:,i] = 0
#     R[i, i] += 6/16

#     R[i-3, i] += 1/16

#     for j in dest:
#         R[j, i] += 1/16

#     found = False    
#     for j in stations:
#         if j > i:
#             R[j, i] += 1/8
#             found = True
#             break

#     if found == False:
#         R[5, i] += 1/8

#     found = False
    
#     for j in utility:
#         if j > i:
#             R[j, i] += 1/16
#             found += True
#             break

#     if found == False:
#         R[12, i] += 1/16

#     if (i == 36):
#         R[:, i] += 1/16 * R[:, i-3]
#         R[i-3, i] =  1/16 * 14/16


# A = R @ M

# eigenvalues, eigenvectors = np.linalg.eig(A)

# order = np.argsort(-np.abs(eigenvalues))
# eigenvalues = eigenvalues[order]

# eigenvectors = eigenvectors[:, order]

# ### starting state u0 = [1, 0, 0, ... 0] because everyone always starts at the Go square

# x = np.zeros(43)
# x[0] = 1

# c = np.linalg.solve(eigenvectors, x)

# for i in range(1000):
#     x = A @ x

# # print(np.allclose(x, c[0]*eigenvectors[:,0]))


# pi = np.real(c[0]*eigenvectors[:,0])

