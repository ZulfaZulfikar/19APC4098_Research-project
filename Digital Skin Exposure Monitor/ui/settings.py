"""
Settings Module
Configuration interface for monitoring parameters.
"""

import tkinter as tk
from tkinter import ttk


class SettingsWindow(tk.Toplevel):
    """Settings configuration window."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Settings")
        self.geometry("700x600")
        self.configure(bg="#f0f0f0")
        
        # Load current settings
        from core.controller import get_monitoring_interval, get_alert_cooldown
        self.current_interval = get_monitoring_interval()
        self.current_cooldown = get_alert_cooldown()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create settings UI widgets."""
        
        # Header
        header_frame = tk.Frame(self, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Settings",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Content
        content_frame = tk.Frame(self, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Monitoring interval
        interval_frame = tk.Frame(content_frame, bg="#f0f0f0")
        interval_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            interval_frame,
            text="Monitoring Interval (seconds):",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#2c3e50",
        ).pack(side=tk.LEFT)
        
        self.interval_var = tk.StringVar(value=str(self.current_interval))
        interval_entry = tk.Entry(
            interval_frame,
            textvariable=self.interval_var,
            width=12,
            font=("Arial", 11),
            bg="#ffffff",
            fg="#2c3e50",
            relief=tk.SUNKEN,
            bd=1,
            justify=tk.CENTER
        )
        interval_entry.pack(side=tk.RIGHT)
        
        # Alert cooldown
        cooldown_frame = tk.Frame(content_frame, bg="#f0f0f0")
        cooldown_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(
            cooldown_frame,
            text="Alert Cooldown (seconds):",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg = "#2c3e50",
        ).pack(side=tk.LEFT)
        
        self.cooldown_var = tk.StringVar(value=str(self.current_cooldown))
        cooldown_entry = tk.Entry(
            cooldown_frame,
            textvariable=self.cooldown_var,
            width=12,
            font=("Arial", 11),
            bg="#ffffff",
            fg="#2c3e50",
            relief=tk.SUNKEN,
            bd=1,
            justify=tk.CENTER
        )
        cooldown_entry.pack(side=tk.RIGHT)
        
        # Info section
        info_frame = tk.LabelFrame(
            content_frame,
            text="Information",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        info_frame.pack(fill=tk.X, pady=20)
        
        info_text = """
        This system monitors:
        • Distance from screen (via webcam)
        • Screen brightness (OS-level)
        • Blue light exposure score
        • Thermal exposure score
        
        Risk levels are calculated based on:
        • Exposure duration
        • Screen proximity
        • Screen brightness
        
        Alerts are shown when risk is HIGH.
        """
        
        info_label = tk.Label(
            info_frame,
            text=info_text.strip(),
            font=("Arial", 9),
            bg="#ffffff",
            fg="#2c3e50",
            justify=tk.LEFT,
            padx=15,
            pady=15,
            relief=tk.FLAT
        )
        info_label.pack(anchor=tk.W, fill=tk.X, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=20)
        
        save_btn = tk.Button(
            button_frame,
            text="Save",
            command=self.save_settings,
            bg="#27ae60",
            # fg="white",
            fg="#2c3e50",
            padx=20,
            pady=8,
            font=("Arial", 11),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="white"
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy,
            bg="#95a5a6",
            # fg="white",
            fg="#2c3e50",
            padx=20,
            pady=8,
            font=("Arial", 11),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#7f8c8d",
            activeforeground="white"
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
    def save_settings(self):
        """Save settings to the controller."""
        import tkinter.messagebox as messagebox
        
        try:
            # Validate and save monitoring interval
            interval_str = self.interval_var.get().strip()
            if not interval_str or not interval_str.isdigit():
                messagebox.showerror("Error", "Monitoring interval must be a positive number.")
                return
            
            interval = int(interval_str)
            if interval < 1:
                messagebox.showerror("Error", "Monitoring interval must be at least 1 second.")
                return
            
            # Validate and save alert cooldown
            cooldown_str = self.cooldown_var.get().strip()
            if not cooldown_str or not cooldown_str.isdigit():
                messagebox.showerror("Error", "Alert cooldown must be a positive number.")
                return
            
            cooldown = int(cooldown_str)
            if cooldown < 0:
                messagebox.showerror("Error", "Alert cooldown cannot be negative.")
                return
            
            # Save to controller
            from core.controller import set_monitoring_interval, set_alert_cooldown
            set_monitoring_interval(interval)
            set_alert_cooldown(cooldown)
            
            messagebox.showinfo("Success", f"Settings saved successfully!\n\nMonitoring Interval: {interval} seconds\nAlert Cooldown: {cooldown} seconds")
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

