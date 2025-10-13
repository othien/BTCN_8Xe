import heapq, itertools
from utils import target_cols_from_pos, step_cost

def astar(target_pos, n):
    target_cols = target_cols_from_pos(target_pos)

    def h(state):
        # lower bound = còn bao nhiêu hàng chưa đặt
        return n - len(state)

    start = tuple()
    counter = itertools.count()
    g0 = 0
    f0 = g0 + h(start)
    pq = [(f0, next(counter), g0, start)]  # (f, tie, g, state)
    best_g = {start: g0}
    parent = {start: None}

    while pq:
        f, _, g, state = heapq.heappop(pq)
        row = len(state)

        if row == n and list(state) == target_cols:
            path = []
            s = state
            while s is not None:
                path.append(s)
                s = parent[s]
            path.reverse()
            return path

        if g > best_g.get(state, float('inf')):
            continue

        if row < n:
            used = set(state)
            for col in range(n):
                if col in used:
                    continue
                child = state + (col,)
                g2 = g + step_cost(row, col, target_cols)
                if g2 < best_g.get(child, float('inf')):
                    best_g[child] = g2
                    parent[child] = state
                    f2 = g2 + h(child)
                    heapq.heappush(pq, (f2, next(counter), g2, child))
    return None
