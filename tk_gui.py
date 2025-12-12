#!/usr/bin/env python3
"""
Tkinter GUI for Disk Scheduling Simulator

Place this file in your repo root and run:
    python tk_gui.py

It expects your simulator package to provide:
  - simulator.disk.Disk(size, head, direction)
  - simulator.algorithms.simulate_fcfs(...)
  - simulate_sstf, simulate_scan, simulate_cscan

If names differ, adjust the imports below.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import math

# --- Try to import your simulator modules ---
try:
    from simulator.disk import Disk
    from simulator.algorithms import (
        simulate_fcfs,
        simulate_sstf,
        simulate_scan,
        simulate_cscan,
    )
except Exception as e:
    # If import fails, provide helpful message in GUI later
    Disk = None
    simulate_fcfs = simulate_sstf = simulate_scan = simulate_cscan = None
    IMPORT_ERROR = str(e)
else:
    IMPORT_ERROR = None

# --- Helper parsing / validation ---
def parse_requests(s):
    try:
        items = [int(x.strip()) for x in s.split(",") if x.strip() != ""]
        return items
    except Exception:
        return None

# --- Main Application ---
class DiskGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Disk Scheduling Simulator (Tkinter)")
        self.geometry("1000x650")
        self.resizable(True, True)

        self.algos = {
            "FCFS": simulate_fcfs,
            "SSTF": simulate_sstf,
            "SCAN": simulate_scan,
            "C-SCAN": simulate_cscan,
        }

        self.current_result = None
        self.animation_running = False
        self.animation_after_id = None
        self.animation_delay_ms = 400

        self._build_ui()

    def _build_ui(self):
        # Top frame for inputs
        top = ttk.Frame(self)
        top.pack(side="top", fill="x", padx=8, pady=6)

        # Left inputs
        left_in = ttk.Frame(top)
        left_in.pack(side="left", anchor="n")

        ttk.Label(left_in, text="Requests (comma-separated):").grid(row=0, column=0, sticky="w")
        self.requests_var = tk.StringVar(value="82,170,43,140,24,16,190")
        self.requests_entry = ttk.Entry(left_in, textvariable=self.requests_var, width=40)
        self.requests_entry.grid(row=1, column=0, padx=4, pady=2, sticky="w")

        ttk.Label(left_in, text="Disk size (tracks, N):").grid(row=2, column=0, sticky="w")
        self.disk_size_var = tk.IntVar(value=200)
        ttk.Entry(left_in, textvariable=self.disk_size_var, width=10).grid(row=3, column=0, sticky="w", padx=4, pady=2)

        ttk.Label(left_in, text="Start head:").grid(row=4, column=0, sticky="w")
        self.head_var = tk.IntVar(value=50)
        ttk.Entry(left_in, textvariable=self.head_var, width=10).grid(row=5, column=0, sticky="w", padx=4, pady=2)

        ttk.Label(left_in, text="Direction (for SCAN variants):").grid(row=6, column=0, sticky="w")
        self.direction_var = tk.StringVar(value="up")
        ttk.Combobox(left_in, textvariable=self.direction_var, values=["up", "down"], width=8).grid(row=7, column=0, sticky="w", padx=4, pady=2)

        ttk.Label(left_in, text="Algorithm:").grid(row=8, column=0, sticky="w", pady=(6,0))
        self.algo_var = tk.StringVar(value="FCFS")
        algo_menu = ttk.Combobox(left_in, textvariable=self.algo_var, values=list(self.algos.keys()), state="readonly", width=15)
        algo_menu.grid(row=9, column=0, sticky="w", padx=4, pady=2)

        run_btn = ttk.Button(left_in, text="Run Simulation", command=self.run_simulation)
        run_btn.grid(row=10, column=0, sticky="w", padx=4, pady=(8,2))

        random_btn = ttk.Button(left_in, text="Random example (8)", command=self.set_random_requests)
        random_btn.grid(row=11, column=0, sticky="w", padx=4, pady=(2,2))

        # Middle controls (play/step/metrics)
        mid = ttk.Frame(top)
        mid.pack(side="left", padx=10)

        controls = ttk.LabelFrame(mid, text="Controls")
        controls.pack(fill="both", padx=4, pady=2)

        self.play_btn = ttk.Button(controls, text="Play", command=self.toggle_animation, width=8)
        self.play_btn.grid(row=0, column=0, padx=6, pady=6)

        ttk.Button(controls, text="Step ▶", command=lambda: self.step_animation(1)).grid(row=0, column=1, padx=6, pady=6)
        ttk.Button(controls, text="Step ◀", command=lambda: self.step_animation(-1)).grid(row=0, column=2, padx=6, pady=6)

        ttk.Label(controls, text="Speed (ms):").grid(row=1, column=0, sticky="e", padx=(6,0))
        self.speed_var = tk.IntVar(value=self.animation_delay_ms)
        ttk.Entry(controls, textvariable=self.speed_var, width=8).grid(row=1, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(controls, text="Step:").grid(row=2, column=0, sticky="e")
        self.step_var = tk.IntVar(value=0)
        self.step_slider = ttk.Scale(controls, from_=0, to=0, orient="horizontal", command=self.on_slider_move, length=240)
        self.step_slider.grid(row=2, column=1, columnspan=2, padx=6, pady=6)

        # Right: metrics
        right_metrics = ttk.LabelFrame(top, text="Metrics")
        right_metrics.pack(side="left", padx=8)
        self.metrics_text = tk.Text(right_metrics, width=36, height=10, wrap="word")
        self.metrics_text.pack(padx=4, pady=4)

        # Middle area: canvas + matplotlib-like simple plot (tk Canvas)
        middle = ttk.Frame(self)
        middle.pack(fill="both", expand=True, padx=8, pady=6)

        # Top: track canvas
        track_frame = ttk.LabelFrame(middle, text="Track view")
        track_frame.pack(side="top", fill="x", expand=False, padx=4, pady=6)
        self.canvas = tk.Canvas(track_frame, height=160, bg="white")
        self.canvas.pack(fill="x", expand=True, padx=6, pady=6)

        # Bottom: simple step table
        table_frame = ttk.LabelFrame(middle, text="Step-by-step")
        table_frame.pack(side="top", fill="both", expand=True, padx=4, pady=6)
        cols = ("Step", "From", "To", "Seek")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=90, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bottom status
        self.status_var = tk.StringVar(value="Ready")
        statusbar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        statusbar.pack(side="bottom", fill="x")

        # If import error, disable controls and show message
        if IMPORT_ERROR is not None:
            self.disable_all()
            messagebox.showerror("Import error", f"Could not import simulator modules:\n{IMPORT_ERROR}\n\nAdjust imports in tk_gui.py to match your project.")

    def disable_all(self):
        for child in self.winfo_children():
            child.configure(state="disabled")

    def set_random_requests(self):
        import random
        n = 8
        size = max(50, self.disk_size_var.get())
        reqs = ",".join(str(random.randint(0, size-1)) for _ in range(n))
        self.requests_var.set(reqs)

    def run_simulation(self):
        # Parse inputs and call simulation function
        req_text = self.requests_var.get()
        requests = parse_requests(req_text)
        if requests is None:
            messagebox.showerror("Input error", "Requests must be comma-separated integers.")
            return
        size = self.disk_size_var.get()
        head = self.head_var.get()
        direction = self.direction_var.get()
        algo_name = self.algo_var.get()
        sim_fn = self.algos.get(algo_name)
        if sim_fn is None:
            messagebox.showerror("Algorithm error", "Selected algorithm not available.")
            return

        # create Disk; direction: 1 for up, -1 for down
        dir_val = -1 if direction == "down" else 1
        try:
            disk = Disk(size=int(size), head=int(head), direction=dir_val)
        except Exception as e:
            messagebox.showerror("Disk error", f"Could not create Disk: {e}")
            return

        try:
            res = sim_fn(requests, disk)
        except Exception as e:
            messagebox.showerror("Simulation error", f"Algorithm raised an error:\n{e}")
            return

        # store result
        self.current_result = res
        # prepare UI for result
        self.populate_metrics(res)
        self.populate_table(res)
        self.prepare_canvas(res, size, requests)
        # configure slider
        max_step = max(0, len(res.positions)-1)
        self.step_slider.config(from_=0, to=max_step)
        self.step_var.set(0)
        self.step_slider.set(0)
        self.status_var.set(f"Ran {algo_name} — {len(res.positions)-1} steps")

    def populate_metrics(self, res):
        self.metrics_text.delete("1.0", tk.END)
        self.metrics_text.insert(tk.END, f"Total seek: {getattr(res, 'total_seek', 'N/A')}\n")
        avg = getattr(res, "average_seek", "N/A")
        if isinstance(avg, float):
            avg = f"{avg:.2f}"
        self.metrics_text.insert(tk.END, f"Average seek: {avg}\n")
        # show steps
        steps = max(0, len(getattr(res, "positions", [])) - 1)
        self.metrics_text.insert(tk.END, f"Steps: {steps}\n")

    def populate_table(self, res):
        # clear
        for r in self.tree.get_children():
            self.tree.delete(r)
        positions = getattr(res, "positions", [])
        for i in range(1, len(positions)):
            frm = positions[i-1]
            to = positions[i]
            seek = abs(to - frm)
            self.tree.insert("", "end", values=(i, frm, to, seek))

    def prepare_canvas(self, res, disk_size, requests):
        # clear canvas
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or self.canvas.winfo_reqwidth() or 800
        h = self.canvas.winfo_height() or 140
        margin = 30
        self._track_x0 = margin
        self._track_x1 = w - margin
        self._track_y = h // 2
        # draw baseline
        self.canvas.create_line(self._track_x0, self._track_y, self._track_x1, self._track_y, fill="#888", width=2)
        # draw request markers
        self._req_positions = []
        for r in requests:
            x = self._map_track_to_x(r, disk_size)
            self.canvas.create_text(x, self._track_y - 14, text=str(r), font=("TkDefaultFont", 8), fill="black")
            self.canvas.create_line(x, self._track_y - 6, x, self._track_y + 6, fill="red", width=2)
            self._req_positions.append((r, x))
        # draw initial head (if positions exist)
        self.draw_head_at_step(0)

    def _map_track_to_x(self, track, disk_size):
        # map track number to canvas x coordinate
        x0 = self._track_x0
        x1 = self._track_x1
        # avoid division by zero
        if disk_size <= 1:
            return (x0 + x1) // 2
        frac = track / (disk_size - 1)
        return int(x0 + frac * (x1 - x0))

    def draw_head_at_step(self, step_idx):
        # remove existing head items
        self.canvas.delete("head_marker")
        if not self.current_result:
            return
        positions = getattr(self.current_result, "positions", [])
        if not positions:
            return
        idx = max(0, min(step_idx, len(positions)-1))
        head_track = positions[idx]
        disk_size = self.disk_size_var.get()
        x = self._map_track_to_x(head_track, disk_size)
        r = 10
        self.canvas.create_oval(x-r, self._track_y-r, x+r, self._track_y+r, fill="blue", tags="head_marker")
        self.canvas.create_text(x, self._track_y + 18, text=f"Head: {head_track}", tags="head_marker")

    def on_slider_move(self, val):
        # slider passes float strings
        idx = int(float(val))
        self.step_var.set(idx)
        self.draw_head_at_step(idx)
        # highlight corresponding row in treeview
        children = self.tree.get_children()
        if children:
            # clear selection
            for c in children:
                self.tree.selection_remove(c)
            # select row with Step == idx
            if idx > 0 and idx <= len(children):
                target = children[idx-1]
                self.tree.selection_set(target)
                self.tree.see(target)

    def toggle_animation(self):
        if self.animation_running:
            self.stop_animation()
        else:
            self.start_animation()

    def start_animation(self):
        if not self.current_result:
            messagebox.showinfo("No simulation", "Run a simulation first.")
            return
        self.animation_running = True
        self.play_btn.config(text="Pause")
        try:
            self.animation_delay_ms = max(50, int(self.speed_var.get()))
        except Exception:
            self.animation_delay_ms = 400
        self._animate_step()

    def stop_animation(self):
        self.animation_running = False
        self.play_btn.config(text="Play")
        if self.animation_after_id:
            try:
                self.after_cancel(self.animation_after_id)
            except Exception:
                pass
            self.animation_after_id = None

    def _animate_step(self):
        if not self.animation_running or not self.current_result:
            return
        positions = getattr(self.current_result, "positions", [])
        if not positions:
            self.stop_animation()
            return
        current = int(self.step_var.get())
        next_idx = current + 1
        if next_idx >= len(positions):
            # loop back to 0
            next_idx = 0
        # update slider and draw
        self.step_slider.set(next_idx)
        self.on_slider_move(next_idx)
        # schedule next
        self.animation_after_id = self.after(self.animation_delay_ms, self._animate_step)

    def step_animation(self, delta):
        if not self.current_result:
            messagebox.showinfo("No simulation", "Run a simulation first.")
            return
        max_step = max(0, len(self.current_result.positions)-1)
        cur = int(self.step_var.get())
        nxt = max(0, min(max_step, cur + delta))
        self.step_slider.set(nxt)
        self.on_slider_move(nxt)

if __name__ == "__main__":
    app = DiskGUI()
    app.mainloop()
