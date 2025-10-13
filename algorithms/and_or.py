from utils import target_cols_from_pos

def and_or_search(target_pos, n):
    target_cols = tuple(target_cols_from_pos(target_pos))
    start = tuple()

    def is_goal(state):
        return len(state) == n and state == target_cols

    def or_search(state, visited):
        if is_goal(state):
            return [state]
        if state in visited:
            return None

        row = len(state)
        used = set(state)
        # ưu tiên cột gần mục tiêu tại hàng hiện tại
        cand = [(abs(col - target_cols[row]), col) for col in range(n) if col not in used]
        cand.sort()

        for _, col in cand:
            child = state + (col,)
            # môi trường xác định -> AND-node có 1 nhánh
            plan = and_search([child], visited | {state})
            if plan is not None:
                return [state] + plan
        return None

    def and_search(states, visited):
        full_plan = []
        for s in states:
            subplan = or_search(s, visited)
            if subplan is None:
                return None
            if not full_plan:
                full_plan = subplan
            else:
                full_plan += subplan[1:]
        return full_plan

    return or_search(start, set())
