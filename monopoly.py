from fractions import Fraction
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd



dice = [1.0/36.0, 1.0/18.0, 1.0/12.0, 1.0/9.0, 5.0/36.0, 1.0/6.0, 5.0/36.0, 1.0/9.0, 1.0/12.0, 1.0/18.0, 1.0/36.0]

cols = 43
rows = 43

A = np.zeros((rows, cols), dtype=float)

for i in range(cols):


### Handles case 1: players jail transition states

    if i == 30:
        A[40][i] = 1.0
        continue
    elif i == 40:
        A[41][40] = 1.0
        continue
    elif i == 41:
        A[42][i] = 1.0
        continue
    elif i == 42:
        A[10][i] = 1.0
        continue

### Handles case 2: the normal case of rolling the dice

    for j in range(i+2, min(i+13, 40)):
        if j == 30:
            A[40][i] = dice[j-i-2]
        else:
            A[j][i] = dice[j-i-2]

### Handles case 3: the player crosses GO


    if i != 39:
        for j in range(0, i+13-40):
            A[j][i] = dice[39-i - 1 + j]
    elif i == 39:
        for j in range(1, 12):
            A[j][i] = dice[j-1]



eigenvalues, eigenvectors = np.linalg.eig(A)

order = np.argsort(-np.abs(eigenvalues))
eigenvalues = eigenvalues[order]

eigenvectors = eigenvectors[:, order]

### starting state u0 = [1, 0, 0, ... 0] because everyone always starts at the Go square

x = np.zeros(43)
x[0] = 1

c = np.linalg.solve(eigenvectors, x)

for i in range(1000):
    x = A @ x

print(np.allclose(x, c[0]*eigenvectors[:,0]))


pi = np.real(c[0]*eigenvectors[:,0])

sum = 0;

for j in pi:
    sum += j;

pi /= sum
