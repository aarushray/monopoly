from markov_matrix import A, cols, pi

import numpy as np


rng = np.random.default_rng(2026)   # fixed seed: same numbers every run

B = 10

checkpoints = [25, 50, 100, 200, 1000]

chance = [7, 22, 36]
community_chest = [2, 17, 33]
stations = np.array([5, 15, 25, 35])
utilities = np.array([12, 28])

def apply_cards(pos, moved):
    ### draws a card for every player who moved and is now on a chance or community chest square
    pos = pos.copy()
 
    ### Chance: 16 cards. 6 stay, 1 jail, 9 move (nearest station is two cards)
    on_chance = moved & np.isin(pos, chance)
    old = pos[on_chance]
    card = rng.integers(0, 16, old.size)
 
    new = old.copy()                                    ### cards 0-5: stay put
    new[card == 6] = 40                                 ### go to jail
    new[card == 7] = 0                                  ### advance to Go
    new[card == 8] = 24                                 ### Trafalgar Square
    new[card == 9] = 39                                 ### Mayfair
    new[card == 10] = 11                                ### Pall Mall
    new[card == 11] = 5                                 ### Kings Cross
    near_station = (card == 12) | (card == 13)          ### nearest station (2 cards), wraps round past Go
    new[near_station] = stations[np.searchsorted(stations, old[near_station], side = "right") % 4]
    near_utility = card == 14                           ### nearest utility, wraps round past Go
    new[near_utility] = utilities[np.searchsorted(utilities, old[near_utility], side = "right") % 2]
    new[card == 15] = old[card == 15] - 3               ### go back 3 spaces
    pos[on_chance] = new                                ### updates chance so cc can take care of square 33

    ### square 36 chance is special because if a player draws move back by 3 steps,
    ### they end up on square 33 which is a community chest square
 
    ### Community Chest: 14/16 stay, 1/16 Go, 1/16 jail
    ### done after chance so that going back 3 from square 36 (onto 33) also draws a community chest card
    on_cc = moved & np.isin(pos, community_chest)
    card = rng.integers(0, 16, on_cc.sum())
 
    new = pos[on_cc].copy()
    new[card == 0] = 0                                  ### advance to Go
    new[card == 1] = 40                                 ### go to jail
    pos[on_cc] = new
 
    return pos

def markov_freq(N):
    x = np.zeros(cols)
    x[0] = 1
    total = np.zeros(cols)
    for i in range(N):
        x = A @ x
        total += x
    return total / N


def simulate(num_of_games, num_turns):
    """Plays num_of_games fresh, independent games of num_turns turns.
    Returns end-of-turn visit counts (games x states) over all turns, and over turns B+1..N."""
    pos = np.zeros(num_of_games, dtype = int)
    jail = np.zeros(num_of_games, dtype = int)
    counts = np.zeros((num_of_games, cols), dtype = int)
    biased_counts = np.zeros((num_of_games, cols), dtype = int)

    for i in range(1, num_turns + 1):
        ### deciding the roll for each turn
        roll1 = np.array(rng.integers(1,7,num_of_games))
        roll2 = np.array(rng.integers(1, 7, num_of_games))

        roll3 = np.array(rng.integers(1,7,num_of_games))
        roll4 = np.array(rng.integers(1, 7, num_of_games))

        roll5 = np.array(rng.integers(1,7,num_of_games))
        roll6 = np.array(rng.integers(1, 7, num_of_games))

    ### Normal player movement

        in_jail = (jail > 0) ### check who's still in jail
        pos = np.where(in_jail, pos, (pos+roll1+roll2)%40) ### free players move

    
    ### Jail states 

        ### deal with the players to be released
        rolled_a_double = (roll1 == roll2) & (in_jail)
        released = (in_jail) & (jail == 3)

        pos = np.where(rolled_a_double | released, 10+roll1+roll2, pos) ### add their roll to their current pos (10: jail tile)

        jail[rolled_a_double] = 0 ### reset their jail count
        jail[released] = 0

        in_jail[released] = False ### reset their jail state ***IMPORTANT
        in_jail[rolled_a_double] = False

        pos = apply_cards(pos, pos<40)

        send_to_jail = (~in_jail) & ((pos == 30) | (pos == 40)) ### landed on go to jail square
        in_jail[send_to_jail] = True


    ### Double and third rolls

        not_eligible = released | rolled_a_double | in_jail ### players just released from jail or in jail currently

        eligible = (~not_eligible) & (roll1 == roll2)

        pos = np.where(eligible, (pos+roll3+roll4)%40, pos)

        pos = apply_cards(pos, eligible)

        send_to_jail = (~in_jail) & ((pos == 30) | (pos == 40)) ### send players to jail if they are on the go to jail tile
        in_jail[send_to_jail] = True ### change their jail state
        not_eligible[send_to_jail] = True ### add the players that just got sent to jail to the list of players

        eligible = (~not_eligible) & (roll3 == roll4) & (roll1 == roll2)

        pos = np.where(eligible, (pos+roll5+roll6)%40, pos)

        pos = apply_cards(pos, eligible)

        send_to_jail = (~in_jail) & ((pos == 30) | (pos == 40))
        in_jail[send_to_jail] = True
        not_eligible[send_to_jail] = True

        consec_double = (~not_eligible) & (roll5 == roll6) & (roll3 == roll4) & (roll1 == roll2)

        pos = np.where(consec_double, 40, pos)
        in_jail[consec_double] = True

        jail = np.where(in_jail, np.where(jail == 3, 0, jail + 1), 0)
        pos = np.where(jail > 0, 39+jail, pos)



        if i == B + 1:
            biased_counts = counts.copy()
        counts[np.arange(num_of_games), pos] += 1

    return counts, counts - biased_counts


def z_scores(counts, N, expected):
    per_game = counts / N
    se = per_game.std(axis = 0, ddof = 1) / np.sqrt(counts.shape[0])
    ok = se > 0                                      # skips state 30, never visited
    return (per_game.mean(axis = 0)[ok] - expected[ok]) / se[ok]


def rmse(err):
    return float(np.sqrt(np.mean((err * 100) ** 2)))   # percentage points

