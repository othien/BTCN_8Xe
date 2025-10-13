def forward_checking(target_pos, n):
    target_cols = [c for (_, c) in target_pos]
    domains = {i: set(range(n)) for i in range(n)}
    cur, used, path = [], set(), []

    def fc(row):
        if row == n:
            path.append(tuple(cur.copy()))
            return cur == target_cols

        for c in list(domains[row]):
            if c in used: 
                continue
            cur.append(c); used.add(c)
            path.append(tuple(cur.copy()))

            # Sao lưu domains để backtrack
            old_domains = {r: domains[r].copy() for r in range(n)}
            # Cập nhật miền của các biến chưa gán
            for r in range(row + 1, n):
                if c in domains[r]:
                    domains[r].remove(c)

            if fc(row + 1):
                return True
            # Phục hồi miền
            domains.update(old_domains)
            cur.pop(); used.remove(c)
        return False

    fc(0)
    return path
