import heapq, itertools
from utils import target_cols_from_pos, step_cost

def ucs(target_pos, n):
    target_cols = target_cols_from_pos(target_pos)
    start = tuple()
    counter = itertools.count()
    pq = [(0, next(counter), start)]   # (g, tie_breaker, state)
    best = {start: 0}
    parent = {start: None}

    while pq:
        g, _, state = heapq.heappop(pq)
        row = len(state)

        if row == n and list(state) == target_cols:
            path = []
            s = state
            while s is not None:
                path.append(s)
                s = parent[s]
            path.reverse()
            return path

        if g > best.get(state, float('inf')):
            continue

        if row < n:
            used_cols = set(state)
            for col in range(n):
                if col in used_cols:
                    continue
                child = state + (col,)
                g2 = g + step_cost(row, col, target_cols)
                if g2 < best.get(child, float('inf')):
                    best[child] = g2
                    parent[child] = state
                    heapq.heappush(pq, (g2, next(counter), child))
    return None
