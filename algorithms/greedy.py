import heapq, itertools
from utils import target_cols_from_pos

def greedy(target_pos, n):
    target_cols = target_cols_from_pos(target_pos)

    def h(state):
        return sum(abs(state[r] - target_cols[r]) for r in range(len(state)))

    start = tuple()
    counter = itertools.count()
    pq = [(h(start), next(counter), start)]
    parent = {start: None}
    best_h = {start: h(start)}

    while pq:
        _, _, state = heapq.heappop(pq)
        row = len(state)

        if row == n and list(state) == target_cols:
            path = []
            s = state
            while s is not None:
                path.append(s)
                s = parent[s]
            path.reverse()
            return path

        if row < n:
            used = set(state)
            # ưu tiên cột gần mục tiêu ở hàng hiện tại
            cand = []
            for col in range(n):
                if col in used:
                    continue
                cand.append((abs(col - target_cols[row]), col))
            cand.sort()

            for _, col in cand:
                child = state + (col,)
                h2 = h(child)
                if h2 < best_h.get(child, float('inf')):
                    best_h[child] = h2
                    parent[child] = state
                    heapq.heappush(pq, (h2, next(counter), child))
    return None
