from config import N as NCONF

def _valid_tuple(state_tuple):
    return len(set(state_tuple)) == len(state_tuple)

def _move_all(state_tuple, n):
    moved = tuple(((c + 1) % n) for c in state_tuple)
    return moved if _valid_tuple(moved) else None

def _add_one(state_tuple, n):
    used = set(state_tuple)
    for c in range(n):
        if c not in used:
            cand = state_tuple + (c,)
            return cand
    return None

def niemtin(target_pos, n=NCONF, max_steps=10000):
    stack = [(), (1,)]
    parent = {}          
    parent[()]  = None
    parent[(1,)] = ()

    seen = set(stack)
    goal = None
    steps = 0
    while stack and steps < max_steps:
        st = stack.pop()
        steps += 1
        if len(st) == n and _valid_tuple(st):
            goal = st
            break

        moved = _move_all(st, n)
        if moved is not None and moved not in seen:
            seen.add(moved)
            parent[moved] = st
            stack.append(moved)

        added = _add_one(st, n)
        if added is not None and added not in seen:
            seen.add(added)
            parent[added] = st
            stack.append(added)

    if goal is None:
        last = st if stack == [] else stack[-1]
        path = []
        while last is not None:
            path.append(last)
            last = parent.get(last)
        path.reverse()
        return path

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path
