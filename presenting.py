from monopoly import pi

import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd

with open(file = "tile names.txt", mode = "r") as f:
    square_names = [line.strip() for line in f if line.strip()]


top = np.argsort(-pi)[:20]
for idx in top:
    print(f"{square_names[idx]:20s} {pi[idx]:.4f}")