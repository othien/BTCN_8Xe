from collections import deque
from utils import target_cols_from_pos

def ac3(target_pos, n):
    target = target_cols_from_pos(target_pos)

    domains = {i: set() for i in range(n)}
    for r in range(n):
        t = target[r]
        dom = {t}
        dom.add((t - 1) % n)
        dom.add((t + 1) % n)
        domains[r] = dom

    arcs = deque((i, j) for i in range(n) for j in range(n) if i != j)

    def revise(domains, xi, xj):
        removed = False
        to_remove = set()
        for x in domains[xi]:
            if all(y == x for y in domains[xj]):
                to_remove.add(x)
        if to_remove:
            domains[xi] -= to_remove
            removed = True
        return removed

    while arcs:
        xi, xj = arcs.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return []
            for xk in range(n):
                if xk != xi and xk != xj:
                    arcs.append((xk, xi))

    assigned = {}
    used_cols = set()
    order = sorted(range(n), key=lambda r: (len(domains[r]), r))  # MRV

    path = []
    for r in order:
        candidates = []
        t = target[r]
        if t in domains[r]:
            candidates.append(t)
        others = sorted([v for v in domains[r] if v != t], key=lambda v: min((v - t) % n, (t - v) % n))
        candidates.extend(others)

        chosen = None
        for v in candidates:
            if v not in used_cols:
                chosen = v
                break
        if chosen is None:
            return []

        assigned[r] = chosen
        used_cols.add(chosen)

        max_row = max(assigned.keys())
        state = tuple(assigned[i] for i in range(max_row + 1))
        path.append(state)

    final = [None] * n
    for r, v in assigned.items():
        final[r] = v
    path[-1] = tuple(final)  

    return path
