# gui_app.py
import tkinter as tk
import random
import time
from tkinter import scrolledtext

from config import *
from utils import board, solutions, cols_to_positions
from algorithms import (
    bfs, dfs, ucs, greedy, astar, dls, ids, and_or,
    sa, hill, beam, ga,
    ac3, backtracking, forward_checking, niemtin, niemtin1phan
)

def pretty_state(t):
    return "[" + ", ".join(f"({i},{t[i]})" for i in range(len(t))) + "]"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Xe")

        # ======= KHỐI TRÊN: 2 BÀN CỜ =======
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)
        self.left  = tk.Canvas(top_frame, width=N * CELL, height=N * CELL, bg="white")
        self.right = tk.Canvas(top_frame, width=N * CELL, height=N * CELL, bg="white")
        self.left.pack(side="left", padx=15)
        self.right.pack(side="left", padx=15)

        # ======= KHỐI NÚT: 2 HÀNG DƯỚI BÀN CỜ =======
        btn_block = tk.Frame(root)
        btn_block.pack(pady=6, fill="x")

        def mk(parent, text, cmd):  # width 12–13 sẽ đẹp với 8–9 nút/hàng
            return tk.Button(parent, text=text, command=cmd, width=13)

        # Hàng 1 — Classical
        row1 = tk.Frame(btn_block); row1.pack(pady=2)
        for text, cmd in [
            ("BFS", self.run_bfs),
            ("DFS", self.run_dfs),
            ("UCS", self.run_ucs),
            ("A*", self.run_astar),
            ("Greedy", self.run_greedy),
            ("DLS", self.run_dls),
            ("IDS", self.run_ids),
            ("AND-OR", self.run_andor),
        ]:
            mk(row1, text, cmd).pack(side="left", padx=3)

        # Hàng 2 — Meta + CSP
        row2 = tk.Frame(btn_block); row2.pack(pady=2)
        for text, cmd in [
            ("SA", self.run_sa),
            ("Hill", self.run_hc),
            ("Beam", self.run_beam),
            ("GA", self.run_ga),
            ("AC-3", self.run_ac3),
            ("BT", self.run_bt),
            ("FC", self.run_fc),
            ("NT", self.run_nt),
            ("NT1P", self.run_nt1p),
        ]:
            mk(row2, text, cmd).pack(side="left", padx=3)

        # ======= KHỐI THÔNG TIN (TRÁI) + RANDOM & CLEAR (PHẢI) =======
        info_tools_frame = tk.Frame(root)
        info_tools_frame.pack(fill="x", padx=10, pady=(4, 6))

        # --- Thông tin thuật toán (trái)
        info_frame = tk.Frame(info_tools_frame)
        info_frame.pack(side="left", anchor="w")

        tk.Label(info_frame, text="THÔNG TIN THUẬT TOÁN", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        sub = tk.Frame(info_frame)
        sub.pack(anchor="w", pady=(4, 6))

        self.alg_var = tk.StringVar(value="—")
        self.time_var = tk.StringVar(value="—")
        self.steps_var = tk.StringVar(value="—")

        tk.Label(sub, text="Thuật toán: ").grid(row=0, column=0, sticky="w")
        tk.Label(sub, textvariable=self.alg_var, font=("Consolas", 10, "bold")).grid(row=0, column=1, sticky="w")
        tk.Label(sub, text="Thời gian:  ").grid(row=1, column=0, sticky="w")
        tk.Label(sub, textvariable=self.time_var, font=("Consolas", 10, "bold")).grid(row=1, column=1, sticky="w")
        tk.Label(sub, text="Độ dài:     ").grid(row=2, column=0, sticky="w")
        tk.Label(sub, textvariable=self.steps_var, font=("Consolas", 10, "bold")).grid(row=2, column=1, sticky="w")

        # tools
        tools_frame = tk.Frame(info_tools_frame)
        tools_frame.pack(side="right", anchor="e", padx=10)
        tk.Button(tools_frame, text="Random Target", command=self.random_solution, width=16).pack(side="left", padx=4)
        tk.Button(tools_frame, text="Clear Log",     command=self.clear_log,      width=16).pack(side="left", padx=4)

        # ======= KHỐI LOG =======
        tk.Label(root, text="Đường đi (các state):", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10)
        self.log_text = scrolledtext.ScrolledText(root, width=110, height=18, font=("Consolas", 10), wrap="none")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # ======= DỮ LIỆU BAN ĐẦU =======
        self.sols = solutions(N)
        self.cur_idx = 0
        self.after_id = None
        self.current_path = None
        self.step_i = 0
        board(self.left)
        board(self.right, positions=self.sols[self.cur_idx])
        self._append_log("Sẵn sàng. Chọn thuật toán để chạy.\n")

    # ====== Helper & Animation ======
    def _append_log(self, s):
        self.log_text.insert("end", s)
        self.log_text.see("end")

    def clear_log(self):
        self.log_text.delete("1.0", "end")

    def cancel_animation(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def random_solution(self):
        self.cancel_animation()
        self.cur_idx = random.randrange(len(self.sols))
        board(self.left)
        board(self.right, positions=self.sols[self.cur_idx])
        self.alg_var.set("—"); self.time_var.set("—"); self.steps_var.set("—")
        self._append_log("\n[Target] Đã chọn target ngẫu nhiên mới.\n")

    def animate_path(self, path):
        self.current_path = path
        self.step_i = 0
        self.next_step()

    def next_step(self):
        if not self.current_path or self.step_i >= len(self.current_path):
            return
        cols = self.current_path[self.step_i]
        highlight = None if self.step_i == 0 else (len(cols)-1, cols[-1], "place")
        board(self.left, positions=cols_to_positions(cols), highlight=highlight)
        self.step_i += 1
        if self.step_i < len(self.current_path):
            self.after_id = self.root.after(STEP_DELAY, self.next_step)

    # ====== Chạy và animate ======
    def _run_and_animate(self, func, name, expects_positions=False):
        self.cancel_animation()
        board(self.left)
        target_pos = self.sols[self.cur_idx]
        self.alg_var.set(name)

        t0 = time.perf_counter()
        result = func(target_pos, n=N) if not expects_positions else func(n=N, k=K, limit=LIMIT, target=target_pos)
        t1 = time.perf_counter()
        self.time_var.set(f"{(t1 - t0) * 1000:.2f} ms")

        if result is None:
            self._append_log(f"\n[{name}] Không tìm thấy đường đi.\n")
            self.steps_var.set("0")
            return

        if expects_positions:
            self.steps_var.set("—")
            board(self.left, positions=result)
            self._append_log(f"\n[{name}] Hoàn tất. (positions={result})\n")
        else:
            self.steps_var.set(str(len(result)))
            self._append_log(f"\n[{name}] {len(result)} state.\n")
            for i, st in enumerate(result):
                self._append_log(f" s{i}: {pretty_state(st)}\n")
            self.animate_path(result)

    # ====== Nút chạy ======
    def run_bfs(self):   self._run_and_animate(bfs.bfs, "BFS")
    def run_dfs(self):   self._run_and_animate(dfs.dfs, "DFS")
    def run_ucs(self):   self._run_and_animate(ucs.ucs, "UCS")
    def run_astar(self): self._run_and_animate(astar.astar, "A*")
    def run_greedy(self):self._run_and_animate(greedy.greedy, "Greedy")
    def run_dls(self):   self._run_and_animate(lambda pos, n: dls.dls_trace(pos, n, LIMIT), "DLS")
    def run_andor(self): self._run_and_animate(and_or.and_or_search, "AND-OR")
    def run_ids(self):   self._run_and_animate(ids.ids, "IDS")
    def run_sa(self):    self._run_and_animate(sa.simulated_annealing, "Simulated Annealing")
    def run_hc(self):    self._run_and_animate(hill.hill_climbing,   "Hill Climbing")
    def run_beam(self):  self._run_and_animate(beam.beam_search,     "Beam Search")
    def run_ga(self):    self._run_and_animate(ga.ga,                 "Genetic Algorithm")

    def run_ac3(self):   self._run_and_animate(ac3.ac3, "AC-3")
    def run_bt(self):    self._run_and_animate(backtracking.backtracking, "Backtracking")
    def run_fc(self):    self._run_and_animate(forward_checking.forward_checking, "Forward Checking")
    def run_nt(self):    self._run_and_animate(niemtin.niemtin, "NT")
    def run_nt1p(self):  self._run_and_animate(niemtin1phan.niemtin1phan, "NT1P")
