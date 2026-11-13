### This file is used to compute the landing matrix because in one turn there can be
### multiple rolls which loses information about squares that were landed on between
### rolls. Hence, the pi vector is not sufficient to reflect the probability
### distribution of landing on all squares. It can only show probability distribution
### of starting on each square at the start of a turn. This definition is also equivalent
### to saying that pi is the probability of ending a turn on a certain square in the
### long run. The latter definition is useful below in the next explanation.

from markov_matrix import A, M, D, F, J, pi, square_names

import numpy as np
import pandas as pd
### A is the landing probability L but with the intemediate states of omitted.
### For example, if I start at square 3 (indexing starts at 1 for this example),
### and I roll a 4 (2+2), then I end up at 7. Then, I roll a non-double like 5
### and end up at 12. The information about the landing probability at 7 is lost
### because MD only gives the landing probability at the end of the turn. 

L = A + D + D @ D

L[:, 40:] = J[:, 40:]
L[40, :40] = A[40, :40]

### v contains the stationary distribution of the probability of a token landing on
### a square

v = L @ pi

order = np.argsort(-v)


# for idx in order[:20]:
#     print(f"{square_names[idx]:<28} {v[idx]:.5f}")



### The sum for each column is 1.19 because the expected number of times to land on
### each square is 5/6 * 1 + 5/36 * 2 + 5/216 * 3 + 1/216 * 3 = 43/36 = 1.19

for j in range(43):
    s = 0
    for i in L[:,j]:
        s += i

# print(df["Probs"])