def backtracking(target_pos, n):
    target_cols = [c for (_, c) in target_pos]
    path, cur, used = [], [], set()

    def backtrack(row):
        if row == n:
            path.append(tuple(cur.copy()))
            return cur == target_cols
        for c in range(n):
            if c in used: 
                continue
            cur.append(c); used.add(c)
            path.append(tuple(cur.copy()))
            if backtrack(row + 1):
                return True
            cur.pop(); used.remove(c)
        return False

    backtrack(0)
    return path
