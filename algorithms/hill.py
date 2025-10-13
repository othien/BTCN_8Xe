import random
from utils import target_cols_from_pos, random_perm, perm_cost, swap_2

def hill_climbing(target_pos, n, max_iter=5000, restarts=2, seed=None):
 
    if seed is not None:
        random.seed(seed)
    target = target_cols_from_pos(target_pos)

    best_path = []
    cur = random_perm(n)
    cur_cost = perm_cost(cur, target)
    best_path.append(cur)

    for _ in range(restarts + 1):
        improved = True
        it = 0
        while improved and it < max_iter:
            improved = False
            it += 1
            idx = list(range(n)); random.shuffle(idx)
            for a in idx:
                for b in idx:
                    if a >= b: continue
                    cand = swap_2(cur, a, b)
                    cst = perm_cost(cand, target)
                    if cst < cur_cost:
                        cur, cur_cost = cand, cst
                        best_path.append(cur)
                        improved = True
                        if cur_cost == 0:
                            return best_path
                        break
                if improved: break
        if cur_cost != 0 and _ < restarts:
            cur = random_perm(n)
            cur_cost = perm_cost(cur, target)
            best_path.append(cur)
    return best_path
