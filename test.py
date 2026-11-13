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
arr2 = np.array([1,2,3])

print(arr2[arr1])



# x = markov_freq(200)

# print("Orange:")
# print("Turns to recoup:", 680/(14*x[16] + 14*x[18] + 16*x[19]+ 200))
# print("Probability:", x[16] + x[18] + x[19])
# print("Rent:", 44)
# print("EV:", 44*(x[16] + x[18] + x[19]), "\n")


# print("Red:")
# print("Turns to recoup:", 680/(18*x[21] + 18*x[23] + 20*x[24]+ 200))
# print("Probability:", x[21] + x[23] + x[24])
# print("Rent:", 18+18+20)
# print("EV:", 56*(x[21] + x[23] + x[24]), "\n")

# print("Purple:")
# print("Turns to recoup:", 750/(35*x[37] + 50*x[39] + 200))
# print("Probability:", x[37] + x[39])
# print("Rent:", 85)
# print("EV:", 85*(x[37] + x[39]), "\n")

# print("Green:")
# print("Turns to recoup:", 920/(26*x[31] + 26*x[32] + 28*x[34] + 200))
# print("Probability:", x[31] + x[32] + x[34])
# print("Rent:", 80)
# print("EV:", 80*(x[31] + x[32] + x[34]))


# ORANGE = [16, 18, 19]
# RED = [21, 23, 24]
# GREEN = [31, 32, 34]
# PURPLE = [37, 39]












# # from monopoly import A

# # import numpy as np

# # rng = np.random.default_rng(0)
# # G = 10000
# # checkpoints = [25, 50, 100, 200, 1000]

# # pos = np.zeros(G, dtype=int)     # board square 0-39
# # jail = np.zeros(G, dtype=int)    # 0 = not in jail, 1/2/3 = Jail 1/2/3
# # counts = np.zeros((G, 43))
# # results = {}

# # for t in range(1, 1001):
# #     roll = rng.integers(1, 7, G) + rng.integers(1, 7, G)   # two dice
# #     in_jail = (jail > 0)
# #     released = (in_jail & (jail == 3))

# #     pos = np.where(in_jail, pos, (pos + roll) % 40)        # only free players move
# #     pos = np.where(released, 10, pos)                      # leaving jail -> square 10
# #     jail = np.where(in_jail, np.where(jail == 3, 0, jail + 1), 0)

# #     sent = (~in_jail) & (pos == 30)                        # landed on Go to Jail
# #     jail[sent] = 1

# #     idx = np.where(jail > 0, 39 + jail, pos)               # jail 1/2/3 -> indices 40/41/42
# #     counts[np.arange(G), idx] += 1

# #     if t in checkpoints:
# #         results[t] = counts.mean(axis=0) / t

# # def exact_freq(N):
# #     x = np.zeros(43); x[0] = 1
# #     total = np.zeros(43)
# #     for i in range(N):
# #         x = A @ x
# #         total += x
# #     return total / N

# # for N in checkpoints:
# #     print(N, np.max(np.abs(results[N] - exact_freq(N))))