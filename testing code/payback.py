import pandas as pd
import numpy as np

from landing_matrix  import v

_RAW = {
    1:  ("Brown",      60,  50, (2, 10, 30, 90, 160, 250)),
    3:  ("Brown",      60,  50, (4, 20, 60, 180, 320, 450)),
    6:  ("Light blue", 100, 50, (6, 30, 90, 270, 400, 550)),
    8:  ("Light blue", 100, 50, (6, 30, 90, 270, 400, 550)),
    9:  ("Light blue", 120, 50, (8, 40, 100, 300, 450, 600)),
    11: ("Pink",       140, 100, (10, 50, 150, 450, 625, 750)),
    13: ("Pink",       140, 100, (10, 50, 150, 450, 625, 750)),
    14: ("Pink",       160, 100, (12, 60, 180, 500, 700, 900)),
    16: ("Orange",     180, 100, (14, 70, 200, 550, 750, 950)),
    18: ("Orange",     180, 100, (14, 70, 200, 550, 750, 950)),
    19: ("Orange",     200, 100, (16, 80, 220, 600, 800, 1000)),
    21: ("Red",        220, 150, (18, 90, 250, 700, 875, 1050)),
    23: ("Red",        220, 150, (18, 90, 250, 700, 875, 1050)),
    24: ("Red",        240, 150, (20, 100, 300, 750, 925, 1100)),
    26: ("Yellow",     260, 150, (22, 110, 330, 800, 975, 1150)),
    27: ("Yellow",     260, 150, (22, 110, 330, 800, 975, 1150)),
    29: ("Yellow",     280, 150, (24, 120, 360, 850, 1025, 1200)),
    31: ("Green",      300, 200, (26, 130, 390, 900, 1100, 1275)),
    32: ("Green",      300, 200, (26, 130, 390, 900, 1100, 1275)),
    34: ("Green",      320, 200, (28, 150, 450, 1000, 1200, 1400)),
    37: ("Dark blue",  350, 200, (35, 175, 500, 1100, 1300, 1500)),
    39: ("Dark blue",  400, 200, (50, 200, 600, 1400, 1700, 2000)),
}

COLOURS = ["Brown", "Light blue", "Pink", "Orange", "Red", "Yellow", "Green", "Dark blue"]

def build_table(_RAW, v):
    df = pd.DataFrame.from_dict(_RAW, orient="index", columns=["Colour", "Property Cost", "House Cost", "Rent"])
    # for i in _RAW:
    df["Probabilities"] = v[df.index]
    return df

def payback_by_prop(df):
    return df["Property Cost"] / (df["Rent"].str[0] * df["Probabilities"])

def payback_by_colour(df):

    out = df.copy()

    data = {
        "Colour": out["Colour"],
        "base": out["Rent"].str[0],
        "h1": out["Rent"].str[1],
        "h2": out["Rent"].str[2],
        "h3": out["Rent"].str[3],
        "h4": out["Rent"].str[4],
        "H5": out["Rent"].str[5],
        "Probabilities": out["Probabilities"]
    }

    tmp_df = pd.DataFrame(data)
    ### double rent when all the properties of a set are owned
    ### prob * rent there + for all props in that colour/total cost

    tmp_df["rent"] = 2*tmp_df["base"]*tmp_df["Probabilities"]
    total_rent = tmp_df.groupby("Colour")["rent"].sum()
    costs = out.groupby("Colour")["Property Cost"].sum()

    s = costs/total_rent

    return s

def payback_by_best_house(df):

    out = df.copy()

    data = {
        "Colour": out["Colour"],
        "base": out["Rent"].str[0],
        "h1": out["Rent"].str[1],
        "h2": out["Rent"].str[2],
        "h3": out["Rent"].str[3],
        "h4": out["Rent"].str[4],
        "H5": out["Rent"].str[5],
        "Probabilities": out["Probabilities"],
        "House Cost": out["House Cost"]
    }

    tmp_df = pd.DataFrame(data)
    ### double rent when all the properties of a set are owned
    ### prob * rent there + for all props in that colour/total cost

    tmp_df["rent"] = 2*tmp_df["base"]*tmp_df["Probabilities"]
    best_props = tmp_df.groupby("Colour")["Probabilities"].idxmax()
    best = tmp_df.loc[best_props.values].set_index("Colour")

    # print(best)

    total_rent = tmp_df.groupby("Colour")["rent"].sum() - best["rent"]

    total_rent += best["h1"] * best["Probabilities"]

    costs = out.groupby("Colour")["Property Cost"].sum() + best["House Cost"]

    s = costs/total_rent

    return s

def payback_by_full_house(df):

    out = df.copy()

    data = {
        "Colour": out["Colour"],
        "base": out["Rent"].str[0],
        "h1": out["Rent"].str[1],
        "h2": out["Rent"].str[2],
        "h3": out["Rent"].str[3],
        "h4": out["Rent"].str[4],
        "H5": out["Rent"].str[5],
        "Probabilities": out["Probabilities"],
    }

    tmp_df = pd.DataFrame(data)
    ### double rent when all the properties of a set are owned
    ### prob * rent there + for all props in that colour/total cost

    tmp_df["rent"] = tmp_df["h1"]*tmp_df["Probabilities"]

    total_rent = tmp_df.groupby("Colour")["rent"].sum()

    costs = out.groupby("Colour")["Property Cost"].sum() + out.groupby("Colour")["House Cost"].sum()

    print(costs)
    s = costs/total_rent

    return s


df = build_table(_RAW, v)
payback_indiv_prop = payback_by_prop(df)
payback_coloured_set = payback_by_colour(df)
payback_set_house = payback_by_best_house(df)
payback_full_house = payback_by_full_house(df)

# print(payback_indiv_prop)
# c = (payback_by_colour(df))
