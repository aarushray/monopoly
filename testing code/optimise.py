import pandas as pd


def develop(df, colour, budget, even_build=True, buy_set=True):
    """Spend `budget` on a colour set, building on the most-landed property first.

    Levels per property: 0 = no houses (set rent), 1-4 = houses, 5 = hotel.
    even_build=True follows the real rule: no property may be more than one
    level ahead of any other in the set, so the 'best' property gets its next
    house only when the others have caught up.
    buy_set=True charges the price of the properties first.

    Returns a dict with the levels, money spent and left, income per turn, payback.
    """
    g = df[df["Colour"] == colour]
    squares = list(g.index)
    land = g["Probabilities"]
    hcost = g["House Cost"].iloc[0]

    set_cost = g["Property Cost"].sum() if buy_set else 0
    money = budget - set_cost
    levels = {sq: 0 for sq in squares}
    if money < 0:
        return {"colour": colour, "affordable": False, "needed": set_cost}

    # most-landed first
    ranking = sorted(squares, key=lambda s: land[s], reverse=True)

    while money >= hcost:
        # properties that are allowed to take the next house
        lowest = min(levels.values())
        allowed = [s for s in ranking
                   if levels[s] < 5 and (not even_build or levels[s] + 1 - lowest <= 1)]
        if not allowed:
            break
        sq = allowed[0]                      # highest-probability allowed property
        levels[sq] += 1
        money -= hcost

    def rent(sq, lv):
        r = g.loc[sq, "Rent"]
        return 2 * r[0] if lv == 0 else r[lv]

    income = sum(land[sq] * rent(sq, lv) for sq, lv in levels.items())
    spent = budget - money
    return {
        "colour": colour,
        "affordable": True,
        "levels": levels,
        "houses": sum(levels.values()),
        "spent": spent,
        "left": money,
        "income_per_turn": income,
        "payback_turns": spent / income,
    }


def develop_all(df, budget, **kw):
    rows = [develop(df, c, budget, **kw) for c in df["Colour"].unique()]
    return pd.DataFrame(rows).set_index("colour")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/home/claude")
    from markov_matrix import A
    from landing_matrix import L, v
    from payback import _RAW

    df = pd.DataFrame.from_dict(_RAW, orient="index",
                                columns=["Colour", "Property Cost", "House Cost", "Rent"])
    df["Probabilities"] = v[df.index]
    pd.set_option("display.width", 140)
    print(develop_all(df, 1000)[["levels", "spent", "left", "income_per_turn", "payback_turns"]].round(2))
    print()
    print(develop_all(df, 1500, even_build=False)[["levels", "income_per_turn"]].round(2))