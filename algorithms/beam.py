import random
from utils import target_cols_from_pos, random_perm, perm_cost, swap_2

def beam_search(target_pos, n, beam_width=6, neighbor_samples=24, max_iters=300, seed=None):
    if seed is not None:
        random.seed(seed)
    target = target_cols_from_pos(target_pos)
    beam = [random_perm(n) for _ in range(beam_width)]
    parents = {s: None for s in beam}
    best = min(beam, key=lambda s: perm_cost(s, target))
    best_cost = perm_cost(best, target)

    if best_cost == 0:
        return _reconstruct(parents, best)

    for _ in range(max_iters):
        pool = []
        for s in beam:
            cand = {s}
            # sinh kề ngẫu nhiên
            for __ in range(neighbor_samples):
                i, j = random.sample(range(n), 2)
                cand.add(swap_2(s, i, j))
            pool.extend(list(cand))

        pool = list({p for p in pool}) 
        pool.sort(key=lambda s: perm_cost(s, target))
        new_beam = []
        for s in pool:
            if len(new_beam) >= beam_width: break
            if s not in parents:
                # gán parent: tìm parent gần nhất
                par = min(beam, key=lambda x: perm_cost(x, target))
                parents[s] = par
            new_beam.append(s)

        beam = new_beam
        cand_best = beam[0]
        cand_cost = perm_cost(cand_best, target)
        if cand_cost < best_cost:
            best, best_cost = cand_best, cand_cost
        if best_cost == 0:
            break

    return _reconstruct(parents, best)

def _reconstruct(parents, s):
    # Duyệt ngược theo parent (nếu parent khong chính xác thì trả chuỗi các best states)
    path = [s]
    seen = set([s])
    cur = s
    while parents.get(cur) is not None and parents[cur] not in seen:
        cur = parents[cur]
        path.append(cur)
        seen.add(cur)
    path.reverse()
    return path
