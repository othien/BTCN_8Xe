# utils.py
import tkinter as tk
import random
from config import *

def solutions(n=N, k=K):
    sols, used_cols, cur = [], set(), []
    def backtrack(row: int):
        if row == n:
            if len(cur) == k:
                sols.append(cur.copy())
            return
        for c in range(n):
            if c in used_cols: 
                continue
            cur.append((row, c)); used_cols.add(c)
            backtrack(row + 1)
            used_cols.remove(c); cur.pop()
    backtrack(0)
    return sols

def board(canvas, n=N, positions=None, highlight=None):
    canvas.delete("all")
    for r in range(n):
        for c in range(n):
            x1, y1 = c * CELL, r * CELL
            x2, y2 = x1 + CELL, y1 + CELL
            fill = "#eee" if (r + c) % 2 == 0 else "#aaa"
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black", width=2)
    if highlight:
        hr, hc, htype = highlight
        x1, y1 = hc * CELL, hr * CELL
        x2, y2 = x1 + CELL, y1 + CELL
        color = "#c7f8c7" if htype == "place" else "#f8c7c7"
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, stipple="gray25", outline="black", width=2)
    if positions:
        for (r, c) in positions:
            cx, cy = c * CELL + CELL // 2, r * CELL + CELL // 2
            canvas.create_text(cx, cy, text=ROOK_TEXT, font=(FONT_NAME, CELL // 2), fill="red")

def cols_to_positions(cols):  # tuple[int] -> list[(row,col)]
    return [(r, cols[r]) for r in range(len(cols))]

def target_cols_from_pos(target_pos):  # list[(row,col)] -> list[int]
    return [c for (_, c) in target_pos]

def step_cost(row, new_col, target_cols):
    return abs(new_col - target_cols[row]) + 1

# ===== tiện ích bổ sung cho các meta-heuristic =====
def random_perm(n):
    return tuple(random.sample(range(n), n))

def perm_cost(state, target_cols):
    """Chi phí của 1 hoán vị so với target: tổng |state[r]-target[r]|."""
    return sum(abs(state[r] - target_cols[r]) for r in range(len(state)))

def swap_2(state, i, j):
    s = list(state)
    s[i], s[j] = s[j], s[i]
    return tuple(s)
