from monopoly import eigenvalues
import numpy as np

np.sort(eigenvalues)

tol = 1e-10

repeats = []

for i in range (np.size(eigenvalues)):
    for j in range(i+1, np.size(eigenvalues)):
        if np.abs(eigenvalues[i]-eigenvalues[j]) < tol:
            repeats.append( (np.round(eigenvalues[i], 5), np.round(eigenvalues[j], 5)) )




for i in eigenvalues:
    if np.abs(i - 0.0) < tol:
        print(i)