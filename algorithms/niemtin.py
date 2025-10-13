from config import N as NCONF
from utils import target_cols_from_pos

def _valid_tuple(state_tuple):
    return len(set(state_tuple)) == len(state_tuple)

def _rotate_toward_target(state, n, target):
    if not state:
        return state
    plus = tuple((c + 1) % n for c in state)
    minus = tuple((c - 1) % n for c in state)
    def cost(s):
        return sum(min((s[i]-target[i]) % n, (target[i]-s[i]) % n) for i in range(len(s)))
    cand = []
    if _valid_tuple(plus):  cand.append((cost(plus), plus))
    if _valid_tuple(minus): cand.append((cost(minus), minus))
    if not cand:
        return state
    cand.sort(key=lambda x: x[0])
    return cand[0][1]

def niemtin(target_pos, n=NCONF, max_steps=10000):
    target = target_cols_from_pos(target_pos)
    state = (target[0],)
    path = [state]
    steps = 0

    for r in range(1, n):
        desired = target[r]
        spin_guard = 0
        while desired in state and steps < max_steps and spin_guard < n * 3:
            new_state = _rotate_toward_target(state, n, target)
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
                cand = [(k - desired) % n for k in range(n) if k not in state]
                cand.sort(key=lambda d: min(d, n - d))
                placed = False
                for d in cand:
                    c = (desired + d) % n
                    trial = state + (c,)
                    if _valid_tuple(trial):
                        state = trial
                        path.append(state)
                        placed = True
                        break
                if not placed:
                    break  
        else:
            break

        if steps >= max_steps:
            break

    return path
