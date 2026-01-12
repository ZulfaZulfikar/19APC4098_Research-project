"""
History View Module
Displays historical exposure data from CSV logs.
"""

import tkinter as tk
from tkinter import ttk
import csv
import os
from datetime import datetime


class HistoryView(tk.Toplevel):
    """Window for viewing historical exposure data."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Exposure History")
        self.geometry("1000x600")
        self.configure(bg="#f0f0f0")
        
        self.log_file = "data/exposure_log.csv"
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """Create UI widgets for history view."""
        
        # Header
        header_frame = tk.Frame(self, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Exposure History",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Content frame
        content_frame = tk.Frame(self, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Toolbar
        toolbar = tk.Frame(content_frame, bg="#f0f0f0")
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        refresh_btn = tk.Button(
            toolbar,
            text="Refresh",
            command=self.load_data,
            bg="#3498db",
            fg="white",
            padx=15,
            pady=6,
            font=("Arial", 10),
            cursor="hand2",
            relief=tk.FLAT,
            activebackground="#2980b9",
            activeforeground="white"
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Treeview for data table
        tree_frame = tk.Frame(content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columns = ("DateTime", "Distance", "Brightness", "BlueScore", "ThermalScore", "BlueRisk", "ThermalRisk")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Configure style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#ffffff",
                       foreground="#2c3e50",
                       fieldbackground="#ffffff",
                       rowheight=25,
                       font=("Arial", 10))
        style.configure("Treeview.Heading",
                       background="#34495e",
                       foreground="white",
                       font=("Arial", 10, "bold"),
                       relief=tk.FLAT)
        style.map("Treeview",
                 background=[("selected", "#3498db")],
                 foreground=[("selected", "white")])
        
        # Column configuration
        self.tree.heading("DateTime", text="Date & Time")
        self.tree.heading("Distance", text="Distance (cm)")
        self.tree.heading("Brightness", text="Brightness (%)")
        self.tree.heading("BlueScore", text="Blue Light Score")
        self.tree.heading("ThermalScore", text="Thermal Score")
        self.tree.heading("BlueRisk", text="Blue Risk")
        self.tree.heading("ThermalRisk", text="Thermal Risk")
        
        self.tree.column("DateTime", width=160, anchor=tk.CENTER)
        self.tree.column("Distance", width=110, anchor=tk.CENTER)
        self.tree.column("Brightness", width=110, anchor=tk.CENTER)
        self.tree.column("BlueScore", width=130, anchor=tk.CENTER)
        self.tree.column("ThermalScore", width=130, anchor=tk.CENTER)
        self.tree.column("BlueRisk", width=110, anchor=tk.CENTER)
        self.tree.column("ThermalRisk", width=110, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
    def load_data(self):
        """Load data from CSV file into the treeview."""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load from CSV
        if not os.path.exists(self.log_file):
            return
            
        try:
            with open(self.log_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    values = (
                        row.get("DateTime", "N/A"),
                        row.get("Distance_cm", "N/A"),
                        row.get("Brightness", "N/A"),
                        row.get("BlueLightScore", "N/A"),
                        row.get("ThermalScore", "N/A"),
                        row.get("BlueRisk", "N/A"),
                        row.get("ThermalRisk", "N/A")
                    )
                    item = self.tree.insert("", tk.END, values=values)
                    
                    # Color code risk levels
                    blue_risk = row.get("BlueRisk", "").upper()
                    thermal_risk = row.get("ThermalRisk", "").upper()
                    
                    # Apply tags based on risk levels
                    if blue_risk == "HIGH" or thermal_risk == "HIGH":
                        self.tree.set(item, "#0", "")  # Apply color to first column
                    elif blue_risk == "MODERATE" or thermal_risk == "MODERATE":
                        self.tree.set(item, "#0", "")  # Apply color to first column
        except Exception as e:
            print(f"Error loading history: {e}")

