"""
Dashboard UI Module
Main GUI dashboard for displaying real-time monitoring metrics.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class Dashboard(tk.Tk):
    """Main dashboard window for the Digital Skin Exposure Monitor."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Digital Skin Exposure Monitor - AI-Driven Tracking System")
        self.geometry("900x700")
        self.configure(bg="#f0f0f0")
        
        # Initialize UI components
        self.create_widgets()
        
        # Current metrics storage
        self.current_data = {}
        
    def create_widgets(self):
        """Create and layout all UI widgets."""
        
        # Header
        header_frame = tk.Frame(self, bg="#2c3e50", height=120)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Digital Skin Exposure Monitor",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="AI-Driven Blue Light & Thermal Exposure Tracking",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Menu buttons
        menu_frame = tk.Frame(header_frame, bg="#2c3e50")
        menu_frame.pack(pady=5)
        
        history_btn = tk.Button(
            menu_frame,
            text="View History",
            command=self.show_history,
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
        history_btn.pack(side=tk.LEFT, padx=5)
        
        settings_btn = tk.Button(
            menu_frame,
            text="Settings",
            command=self.show_settings,
            bg="#95a5a6",
            fg="white",
            padx=15,
            pady=6,
            font=("Arial", 10),
            cursor="hand2",
            relief=tk.FLAT,
            activebackground="#7f8c8d",
            activeforeground="white"
        )
        settings_btn.pack(side=tk.LEFT, padx=5)
        
        # Main content area
        content_frame = tk.Frame(self, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Metrics section
        metrics_frame = tk.LabelFrame(
            content_frame,
            text="Current Metrics",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=20,
            pady=20
        )
        metrics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Distance metric
        self.create_metric_row(
            metrics_frame,
            "Distance from Screen",
            "distance",
            "cm",
            "#2c3e50"
        )
        
        # Brightness metric
        self.create_metric_row(
            metrics_frame,
            "Screen Brightness",
            "brightness",
            "%",
            "#f39c12"
        )
        
        # Session duration
        self.create_metric_row(
            metrics_frame,
            "Session Duration",
            "duration_min",
            "min",
            "#95a5a6"
        )
        
        # Exposure scores section
        scores_frame = tk.LabelFrame(
            content_frame,
            text="Exposure Scores & Risk Assessment",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=20,
            pady=20
        )
        scores_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Blue light score
        self.create_score_row(
            scores_frame,
            "Blue Light Exposure",
            "blue_score",
            "blue_risk",
            "#9b59b6"
        )
        
        # Thermal score
        self.create_score_row(
            scores_frame,
            "Thermal Exposure",
            "thermal_score",
            "thermal_risk",
            "#e74c3c"
        )
        
        # Status bar
        status_frame = tk.Frame(self, bg="#34495e", height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="System Initializing...",
            font=("Arial", 9),
            bg="#34495e",
            fg="white"
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.time_label = tk.Label(
            status_frame,
            text="",
            font=("Arial", 9),
            bg="#34495e",
            fg="white"
        )
        self.time_label.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # Update time label
        self.update_time()
        
    def create_metric_row(self, parent, label_text, key, unit, color):
        """Create a metric display row."""
        row_frame = tk.Frame(parent, bg="#f0f0f0")
        row_frame.pack(fill=tk.X, pady=12)
        
        label = tk.Label(
            row_frame,
            text=label_text + ":",
            font=("Arial", 11),
            fg="#2c3e50",
            bg="#f0f0f0",
            width=20,
            anchor="w"
        )
        label.pack(side=tk.LEFT)
        
        value_label = tk.Label(
            row_frame,
            text="--",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg=color,
            width=12,
            anchor="w",
            relief=tk.FLAT,
            padx=8,
            pady=4
        )
        value_label.pack(side=tk.LEFT, padx=10)
        
        unit_label = tk.Label(
            row_frame,
            text=unit,
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#7f8c8d",
            anchor="w"
        )
        unit_label.pack(side=tk.LEFT)
        
        # Store reference for updates
        setattr(self, f"{key}_label", value_label)
        setattr(self, f"{key}_unit", unit_label)
        
    def create_score_row(self, parent, label_text, score_key, risk_key, color):
        """Create a score and risk display row."""
        row_frame = tk.Frame(parent, bg="#f0f0f0")
        row_frame.pack(fill=tk.X, pady=12)
        
        label = tk.Label(
            row_frame,
            text=label_text + ":",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#2c3e50",
            width=20,
            anchor="w"
        )
        label.pack(side=tk.LEFT)
        
        score_label = tk.Label(
            row_frame,
            text="--",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg=color,
            width=10,
            anchor="w",
            relief=tk.FLAT,
            padx=8,
            pady=4
        )
        score_label.pack(side=tk.LEFT, padx=10)
        
        risk_label = tk.Label(
            row_frame,
            text="--",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            width=12,
            anchor="w",
            relief=tk.FLAT,
            padx=8,
            pady=4
        )
        risk_label.pack(side=tk.LEFT, padx=10)
        
        # Store references
        setattr(self, f"{score_key}_label", score_label)
        setattr(self, f"{risk_key}_label", risk_label)
        
    def update_metrics(self, data):
        """
        Update dashboard with new monitoring data.
        
        Args:
            data (dict): Monitoring data dictionary
        """
        self.current_data = data
        
        # Update distance
        distance = data.get("distance")
        if distance:
            # Use blue for normal distance, red if too close
            distance_color = "#2c3e50" if distance >= 50 else "#e74c3c"
            self.distance_label.config(text=f"{distance:.1f}", fg=distance_color, bg="#ffffff")
        else:
            self.distance_label.config(text="No face detected", fg="#e74c3c", bg="#ffffff")
            
        # Update brightness
        brightness = data.get("brightness")
        if brightness is not None:
            self.brightness_label.config(text=f"{brightness}", bg="#ffffff")
        else:
            self.brightness_label.config(text="N/A", fg="#95a5a6", bg="#ffffff")
            
        # Update duration
        duration = data.get("duration_min", 0)
        self.duration_min_label.config(text=f"{duration}", bg="#ffffff")
        
        # Update blue light score and risk
        blue_score = data.get("blue_score", 0)
        blue_risk = data.get("blue_risk", "UNKNOWN")
        self.blue_score_label.config(text=f"{blue_score:.1f}", bg="#ffffff")
        
        risk_color = {"LOW": "#27ae60", "MODERATE": "#f39c12", "HIGH": "#e74c3c"}.get(blue_risk, "#95a5a6")
        risk_bg = {"LOW": "#d5f4e6", "MODERATE": "#fef5e7", "HIGH": "#fadbd8"}.get(blue_risk, "#ecf0f1")
        self.blue_risk_label.config(text=blue_risk, fg=risk_color, bg=risk_bg)
        
        # Update thermal score and risk
        thermal_score = data.get("thermal_score", 0)
        thermal_risk = data.get("thermal_risk", "UNKNOWN")
        self.thermal_score_label.config(text=f"{thermal_score:.1f}", bg="#ffffff")
        
        risk_color = {"LOW": "#27ae60", "MODERATE": "#f39c12", "HIGH": "#e74c3c"}.get(thermal_risk, "#95a5a6")
        risk_bg = {"LOW": "#d5f4e6", "MODERATE": "#fef5e7", "HIGH": "#fadbd8"}.get(thermal_risk, "#ecf0f1")
        self.thermal_risk_label.config(text=thermal_risk, fg=risk_color, bg=risk_bg)
        
        # Update status
        if distance and brightness:
            self.status_label.config(text="✓ Monitoring Active")
        elif not distance:
            self.status_label.config(text="⚠ Face not detected - Position yourself in front of camera")
        else:
            self.status_label.config(text="⚠ Some sensors unavailable")
            
    def update_time(self):
        """Update the time label in status bar."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)
    
    def show_history(self):
        """Open history view window."""
        from ui.history import HistoryView
        history_window = HistoryView(self)
    
    def show_settings(self):
        """Open settings window."""
        from ui.settings import SettingsWindow
        settings_window = SettingsWindow(self)
        
    def on_closing(self):
        """Handle window closing event."""
        from core.controller import shutdown
        shutdown()
        self.destroy()


if __name__ == "__main__":
    # Test dashboard
    app = Dashboard()
    app.mainloop()

