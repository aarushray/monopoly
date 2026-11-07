
# i = 5
# dice = [1.0/36.0, 1.0/18.0, 1.0/12.0, 1.0/9.0, 5.0/36.0, 1.0/6.0, 5.0/36.0, 1.0/9.0, 1.0/12.0, 1.0/18.0, 1.0/36.0]
# dice *= 36


# starting_idx = (i+2)%40
# counter = 0

# starting_idx = (i+2)%40
# for counter in range(0, 11):
#     if starting_idx == 30:
#         if counter % 2 == 0:
#             print(40, 1)
#     else:
#         if counter % 2 == 0:
#             print(starting_idx, 1)
#     starting_idx += 1
#     if starting_idx > 39:
#         starting_idx %= 40

# for i in range(cols):
# ### Handles case 1: players jail transition states
# ### The rules state that when you throw doubles to
# ### get out of jail, you advance by that number of
# ### squares, but you do not get another roll
# ### So this makes sense
#     if i == 30:
#         M[40][i] = 5.0/6.0
#     elif i == 40 or i == 41:
#         for j in range(12, 23, 2):
#             M[j][i] = 1.0/36.0
#         M[i+1][i] = 5.0/6.0
#     elif i == 42:
#         for j in range(12, 23):
#             M[j][i] = dice[j-12]
#     else:
# ### Handles case 2: the normal case of rolling the dice