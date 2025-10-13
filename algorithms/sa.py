import math, random
from utils import target_cols_from_pos, random_perm, perm_cost, swap_2

def simulated_annealing(target_pos, n, T0=20.0, alpha=0.995, steps=20000, seed=None):
    if seed is not None:
        random.seed(seed)
    target = target_cols_from_pos(target_pos)
    cur = random_perm(n)
    cur_cost = perm_cost(cur, target)
    T = T0

    path = [cur]
    for _ in range(steps):
        i, j = random.sample(range(n), 2)
        nxt = swap_2(cur, i, j)
        delta = perm_cost(nxt, target) - cur_cost
        if delta <= 0 or random.random() < math.exp(-delta / max(T, 1e-9)):
            cur, cur_cost = nxt, cur_cost + delta
            path.append(cur)
            if cur_cost == 0:
                break
        T *= alpha
        if T < 1e-6: T = 1e-6
    return path if perm_cost(path[-1], target) == 0 else path
