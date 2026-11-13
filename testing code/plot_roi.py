from payback import payback_coloured_set, payback_indiv_prop, payback_set_house, payback_full_house       # per-opponent payback, indexed by colour
import matplotlib.pyplot as plt
import numpy as np

num_of_players = 4
opps = num_of_players - 1
game_length = 35                                   # assumed turns per player

x = np.linspace(0, 100, 450)

# board order, so the legend reads like the board
colour_order = ["Brown", "Light blue", "Pink", "Orange", "Red", "Yellow", "Green", "Dark blue"]
color_mapping = {
    "Brown": "#8B4513", "Light blue": "#4FB3E8", "Pink": "#E75480", "Orange": "#F28C28",
    "Red": "#D62728", "Yellow": "#C9A800", "Green": "#2E8B57", "Dark blue": "#1F2C9E",
}


def plot_roi(ax, payback, title):
    """ROI(N) = N / a - 1, where a = payback / opponents (turns to pay back in this game)."""
    for label in colour_order:
        a = payback[label] / opps
        ax.plot(x, x / a - 1, label=f"{label} ({a:.0f} turns)",
                color=color_mapping[label], linewidth=2)
    ax.axhline(0, color="black", linewidth=1)                       # break-even
    ax.axvline(game_length, color="grey", linewidth=1, linestyle="--")
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("Turns")
    ax.set_ylabel("ROI = (rent collected - cost) / cost")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend(title="Colour set (payback)", loc="upper left",
              bbox_to_anchor=(1.02, 1), fontsize=9)


fig1, ax1 = plt.subplots(figsize=(10, 5))
plot_roi(ax1, payback_full_house, f"ROI by colour set, one house on each property ({num_of_players} players)")
plt.tight_layout()
plt.show()

fig2, ax2 = plt.subplots(figsize=(10, 5))
plot_roi(ax2, payback_set_house, f"ROI by colour set, one house on the best property ({num_of_players} players)")
plt.tight_layout()
plt.show()