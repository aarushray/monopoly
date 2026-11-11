from monopoly import A, cols, pi

import numpy as np


# rng = np.random.default_rng()
# num_of_games = 6

# # jail = np.zeros(cols)

# pos = np.zeros(num_of_games, dtype = int)
# jail = np.array([1,2,0,2,0,0,0])
# counts = np.zeros((num_of_games, cols),dtype=int)

# checkpoints = [25, 50, 100, 200, 1000]
# results = {}

# ### Equivalent of modelling a 1000 25-turn, 1000 50-turn, 1000 100-turn, 1000 200-turn, 1000 1000-turn games

# for i in range(1, 2):

#     ### deciding the roll for each turn
#     roll1 = np.array([1,2,3,4,5,6,7])
#     roll2 = np.array([7,6,5,4,3,2,1])

#     ### check who's in jail and who needs to be released
#     rolled_a_double = (roll1 == roll2)
#     print(rolled_a_double)
#     in_jail = (jail > 0)
#     in_jail[rolled_a_double] = False
#     jail[rolled_a_double] = 0
#     released = (in_jail) & (jail == 3)

#     print(jail)



arr1 = np.array([True, False, True])
arr2 = ~arr1

arr3 = arr1 | arr2

print(arr1, arr2, arr3)