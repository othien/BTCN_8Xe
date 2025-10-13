from utils import target_cols_from_pos

def dfs(target_pos, n):
    target_cols = tuple(target_cols_from_pos(target_pos))
    start = tuple()
    stack = [start]
    parent = {start: None}
    visited = set()

    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)

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
            for col in reversed(range(n)):
                if col in used:
                    continue
                child = state + (col,)
                if child not in parent:
                    parent[child] = state
                    stack.append(child)
    return None
