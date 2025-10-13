import random
from utils import target_cols_from_pos, random_perm, perm_cost

def ga(target_pos, n, pop_size=40, generations=300, cx_rate=0.9, mut_rate=0.2, tournament=3, seed=None):
    if seed is not None:
        random.seed(seed)
    target = target_cols_from_pos(target_pos)

    def fitness(s): return -perm_cost(s, target)

    def tournament_sel(pop):
        cand = random.sample(pop, tournament)
        cand.sort(key=fitness, reverse=True)
        return cand[0]

    def ox(p1, p2):
        a, b = sorted(random.sample(range(n), 2))
        child = [None]*n
        child[a:b+1] = p1[a:b+1]
        fill = [x for x in p2 if x not in child]
        j = 0
        for i in range(n):
            if child[i] is None:
                child[i] = fill[j]; j += 1
        return tuple(child)

    def mutate(s):
        if random.random() < mut_rate:
            i, j = random.sample(range(n), 2)
            s = list(s); s[i], s[j] = s[j], s[i]
            return tuple(s)
        return s

    # khởi tạo
    pop = [random_perm(n) for _ in range(pop_size)]
    best = min(pop, key=lambda s: perm_cost(s, target))
    best_path = [best]

    if perm_cost(best, target) == 0:
        return best_path

    for _ in range(generations):
        new_pop = []
        while len(new_pop) < pop_size:
            p1, p2 = tournament_sel(pop), tournament_sel(pop)
            if random.random() < cx_rate:
                c = ox(p1, p2)
            else:
                c = p1
            c = mutate(c)
            new_pop.append(c)
        pop = new_pop
        cand = min(pop, key=lambda s: perm_cost(s, target))
        if perm_cost(cand, target) <= perm_cost(best, target):
            best = cand
            best_path.append(best)
        if perm_cost(best, target) == 0:
            break
    return best_path
