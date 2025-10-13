
from config import N as NCONF
from utils import target_cols_from_pos

def _valid_tuple(state_tuple):
    return len(set(state_tuple)) == len(state_tuple)

def _move_partial(state_tuple, n, fixed_rows):
    moved = list(state_tuple)
    for r in range(len(moved)):
        if r not in fixed_rows:
            moved[r] = (moved[r] + 1) % n
    moved = tuple(moved)
    return moved if _valid_tuple(moved) else None

def _add_one(state_tuple, n):
    used = set(state_tuple)
    for c in range(n):
        if c not in used:
            return state_tuple + (c,)
    return None

def niemtin1phan(target_pos, n=NCONF, max_steps=10000):
    target_cols = target_cols_from_pos(target_pos)
    init = (target_cols[0],)    
    fixed_rows = {0}

    stack = [init]
    parent = {init: None}
    seen = set(stack)
    goal = None
    steps = 0

    while stack and steps < max_steps:
        st = stack.pop()
        steps += 1
        if len(st) == n and _valid_tuple(st):
            goal = st
            break

        moved = _move_partial(st, n, fixed_rows)
        if moved is not None and moved not in seen:
            seen.add(moved)
            parent[moved] = st
            stack.append(moved)

        added = _add_one(st, n)
        if added is not None and added not in seen:
            seen.add(added)
            parent[added] = st
            stack.append(added)

    last = goal if goal is not None else st
    path = []
    while last is not None:
        path.append(last)
        last = parent.get(last)
    path.reverse()
    return path
