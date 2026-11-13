import numpy as np

from MC import checkpoints, markov_freq, simulate, z_scores, rmse, B, pi







games_per_batch = 10000
num_batches = 40          # 40 independent batches per checkpoint

print("N | RMSE vs markov_freq(N) | RMSE after burn-in vs pi | pooled z: mean, sd, %>2, %>3, max")
for N in checkpoints:
    expected = markov_freq(N)
    all_z, r_matrix, r_burn = [], [], []
    for b in range(num_batches):                      # brand-new games for every batch and every N
        counts, counts_after_B = simulate(games_per_batch, N)
        all_z.append(z_scores(counts, N, expected))
        r_matrix.append(rmse(expected - counts.mean(axis = 0) / N))
        if N > B:
            r_burn.append(rmse(pi - counts_after_B.mean(axis = 0) / (N - B)))
    z = np.concatenate(all_z)
    burn = f"{np.mean(r_burn):.4f}" if r_burn else "-"
    print(N, f"{np.mean(r_matrix):.4f}", burn,
          f"{z.mean():+.3f} {z.std():.3f} {100*np.mean(np.abs(z)>2):.1f}% {100*np.mean(np.abs(z)>3):.2f}% {np.abs(z).max():.2f}")