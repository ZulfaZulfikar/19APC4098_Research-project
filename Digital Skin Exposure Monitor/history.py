import tkinter as tk
from tkinter import ttk

class HistoryWindow:
    def __init__(self):
        win = tk.Toplevel()
        win.title("Exposure History")
        win.geometry("700x400")

        cols = ("Date", "Blue Light", "Thermal", "Risk")
        tree = ttk.Treeview(win, columns=cols, show="headings")

        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center")

        tree.pack(fill="both", expand=True)

        sample_data = [
            ("2026-01-05", "68", "50", "Moderate"),
            ("2026-01-06", "80", "65", "High"),
            ("2026-01-07", "45", "40", "Low"),
        ]

        for row in sample_data:
            tree.insert("", "end", values=row)
