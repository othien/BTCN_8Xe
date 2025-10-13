def dls_path(target_cols, limit, n):
    start = tuple()
    parent = {start: None}
    stack = [(start, 0)]

    while stack:
        state, depth = stack.pop()
        if len(state) == n and state == target_cols:
            path = []
            s = state
            while s is not None:
                path.append(s)
                s = parent[s]
            path.reverse()
            return path

        if depth == limit:
            continue

        if len(state) < n:
            used = set(state)
            for col in reversed(range(n)):
                if col in used:
                    continue
                child = state + (col,)
                if child not in parent:
                    parent[child] = state
                    stack.append((child, depth + 1))
    return None


from utils import target_cols_from_pos

def ids(target_pos, n, max_limit=None):
    target_cols = tuple(target_cols_from_pos(target_pos))
    if max_limit is None:
        max_limit = n
    for limit in range(0, max_limit + 1):
        path = dls_path(target_cols, limit, n)
        if path is not None:
            return path
    return None
