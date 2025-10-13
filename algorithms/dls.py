
def dls_trace(target_pos, n, limit):

    target_cols = [c for (_, c) in target_pos]
    path = []           
    used = set()       
    solved = [False]    # flag

    def rec(row, depth, state):
        path.append(tuple(state)) 
        if solved[0]:
            return True

        #đạt độ sâu/hết hàng, kiểm tra nghiệm
        if row == n:
            if list(state) == target_cols:
                solved[0] = True
                return True
            return False
        if depth == limit:
            return False

        # Thử từng cột
        for c in range(n):
            if c in used:
                continue

            used.add(c)
            state.append(c)

            if rec(row + 1, depth + 1, state):
                return True

            # Backtrack: xoá bước vừa đi
            state.pop()
            used.remove(c)
            path.append(tuple(state))  # ghi lại trạng thái lùi

        return False

    rec(0, 0, [])
    return path
