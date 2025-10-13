from collections import deque

def ac3(target_pos, n):
    domains = {i: set(range(n)) for i in range(n)}
    arcs = deque([(i, j) for i in range(n) for j in range(n) if i != j])
    steps = [dict(domains)]

    while arcs:
        (xi, xj) = arcs.popleft()
        if revise(domains, xi, xj):
            steps.append(dict(domains))
            if not domains[xi]:
                return steps
            for xk in range(n):
                if xk != xi and xk != xj:
                    arcs.append((xk, xi))
    return steps

def revise(domains, xi, xj):
    revised = False
    remove_vals = set()
    for x in domains[xi]:
        if all(x == y for y in domains[xj]):  # tất cả giá trị của xj đều trùng x
            remove_vals.add(x)
    if remove_vals:
        domains[xi] -= remove_vals
        revised = True
    return revised
