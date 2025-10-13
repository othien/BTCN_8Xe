from config import N as NCONF
from utils import target_cols_from_pos

def _valid_tuple(state_tuple):
    return len(set(state_tuple)) == len(state_tuple)

def _rotate_partial_toward(state, n, target, fixed_rows):
    if not state:
        return state
    def apply(delta):
        s = list(state)
        for r in range(len(s)):
            if r not in fixed_rows:
                s[r] = (s[r] + delta) % n
        return tuple(s)
    plus  = apply(+1)
    minus = apply(-1)

    def cost(s):
        return sum(min((s[i]-target[i]) % n, (target[i]-s[i]) % n) for i in range(len(s)))

    cand = []
    if _valid_tuple(plus):  cand.append((cost(plus), plus))
    if _valid_tuple(minus): cand.append((cost(minus), minus))
    if not cand:
        return state
    cand.sort(key=lambda x: x[0])
    return cand[0][1]

def niemtin1phan(target_pos, n=NCONF, max_steps=10000):
    target = target_cols_from_pos(target_pos)
    fixed_rows = {0}

    state = (target[0],)  
    path = [state]
    steps = 0

    for r in range(1, n):
        desired = target[r]
        spin_guard = 0
        while desired in state and steps < max_steps and spin_guard < n * 3:
            new_state = _rotate_partial_toward(state, n, target, fixed_rows)
            if new_state == state:
                break
            state = new_state
            path.append(state)
            steps += 1
            spin_guard += 1

        if desired not in state:
            new_state = state + (desired,)
            if _valid_tuple(new_state):
                state = new_state
                path.append(state)
            else:
                for k in range(n):
                    if k in state: 
                        continue
                    trial = state + (k,)
                    if _valid_tuple(trial):
                        state = trial
                        path.append(state)
                        break
        else:
            break

        if steps >= max_steps:
            break

    return path
