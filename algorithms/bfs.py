from collections import deque
from utils import target_cols_from_pos

def bfs(target_pos, n):
    target_cols = tuple(target_cols_from_pos(target_pos))
    start = tuple()
    q = deque([start])
    parent = {start: None}

    while q:
        state = q.popleft()
        if len(state) == n and state == target_cols:
            path = []
            s = state
            while s is not None:
                path.append(s)
                s = parent[s]
            path.reverse()
            return path

        if len(state) < n:
            used = set(state)
            for col in range(n):
                if col in used:
                    continue
                child = state + (col,)
                if child not in parent:
                    parent[child] = state
                    q.append(child)
    return None
