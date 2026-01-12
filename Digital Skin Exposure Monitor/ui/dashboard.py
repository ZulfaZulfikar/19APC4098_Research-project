"""
Dashboard UI Module
Main GUI dashboard for displaying real-time monitoring metrics.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import cv2
from PIL import Image, ImageTk
import numpy as np


class Dashboard(tk.Tk):
    """Main dashboard window for the Digital Skin Exposure Monitor."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Digital Skin Exposure Monitor - AI-Driven Tracking System")
        self.geometry("1000x750")
        self.configure(bg="#f0f0f0")
        
        # Initialize UI components
        self.create_widgets()
        
        # Current metrics storage
        self.current_data = {}
        
        # Camera feed for display
        self.camera_cap = None
        self.camera_updating = False
        self._camera_error_shown = False

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
            # fg="white",
            fg="#2c3e50",
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
            # fg="white",
            fg="#2c3e50",
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

        # Current Metrics section (matching the sketch)
        metrics_frame = tk.LabelFrame(
            content_frame,
            text="Current Matrix",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=20,
            pady=20
        )
        metrics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Left side: Input fields
        left_frame = tk.Frame(metrics_frame, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Distance metric
        self.create_metric_row(
            left_frame,
            "Distance from Screen",
            "distance",
            "cm",
            "#2c3e50"
        )

        # Brightness metric
        self.create_metric_row(
            left_frame,
            "Screen Brightness",
            "brightness",
            "%",
            "#f39c12"
        )

        # Session duration
        self.create_metric_row(
            left_frame,
            "Session Duration",
            "duration_min",
            "min",
            "#95a5a6"
        )

        # Right side: Camera view
        right_frame = tk.Frame(metrics_frame, bg="#f0f0f0")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        camera_label_frame = tk.Label(
            right_frame,
            text="Camera View",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        camera_label_frame.pack(pady=(0, 5))

        # Camera display area
        self.camera_label = tk.Label(
            right_frame,
            text="Initializing camera...",
            bg="#2c3e50",
            fg="white",
            width=40,
            height=15,
            font=("Arial", 9),
            relief=tk.SUNKEN,
            bd=2
        )
        self.camera_label.pack(fill=tk.BOTH, expand=True)

        # Start camera feed after a short delay to ensure camera is initialized
        self.after(500, self.start_camera_feed)

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

        # Left side: Exposure scores
        scores_left = tk.Frame(scores_frame, bg="#f0f0f0")
        scores_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Blue light score
        self.create_score_row(
            scores_left,
            "Blue Light Exposure",
            "blue_score",
            "blue_risk",
            "#9b59b6"
        )

        # Thermal score
        self.create_score_row(
            scores_left,
            "Thermal Exposure",
            "thermal_score",
            "thermal_risk",
            "#e74c3c"
        )

        # Right side: Risk Type
        risk_type_frame = tk.Frame(scores_frame, bg="#f0f0f0")
        risk_type_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        risk_type_label_frame = tk.Label(
            risk_type_frame,
            text="Risk Type",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        risk_type_label_frame.pack(pady=(0, 10))

        # Overall risk type display
        self.risk_type_display = tk.Label(
            risk_type_frame,
            text="--",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            width=15,
            height=5,
            relief=tk.SUNKEN,
            bd=2,
            anchor=tk.CENTER
        )
        self.risk_type_display.pack(fill=tk.BOTH, expand=True)

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

        # Calculate and display overall Risk Type (highest risk)
        overall_risk = self.calculate_overall_risk(blue_risk, thermal_risk)
        risk_type_color = {"LOW": "#27ae60", "MODERATE": "#f39c12", "HIGH": "#e74c3c"}.get(overall_risk, "#95a5a6")
        risk_type_bg = {"LOW": "#d5f4e6", "MODERATE": "#fef5e7", "HIGH": "#fadbd8"}.get(overall_risk, "#ecf0f1")
        self.risk_type_display.config(text=overall_risk, fg=risk_type_color, bg=risk_type_bg)

        # Update status
        if distance and brightness:
            self.status_label.config(text="✓ Monitoring Active")
        elif not distance:
            self.status_label.config(text="⚠ Face not detected - Position yourself in front of camera")
        else:
            self.status_label.config(text="⚠ Some sensors unavailable")

    def calculate_overall_risk(self, blue_risk, thermal_risk):
        """Calculate overall risk type (highest of blue and thermal)."""
        risk_levels = {"LOW": 1, "MODERATE": 2, "HIGH": 3, "UNKNOWN": 0}
        blue_level = risk_levels.get(blue_risk, 0)
        thermal_level = risk_levels.get(thermal_risk, 0)

        max_level = max(blue_level, thermal_level)
        if max_level == 3:
            return "HIGH"
        elif max_level == 2:
            return "MODERATE"
        elif max_level == 1:
            return "LOW"
        else:
            return "UNKNOWN"

    def start_camera_feed(self):
        """Start the camera feed update loop."""
        try:
            from inputs.distance import initialize_camera
            # Ensure camera is initialized
            cap = initialize_camera()
            if cap is None or not cap.isOpened():
                self.camera_label.config(text="Camera not available", fg="white", bg="#2c3e50")
                # Retry after 2 seconds
                self.after(2000, self.start_camera_feed)
                return
            # Reset error flag
            self._camera_error_shown = False
            self.update_camera_feed()
        except Exception as e:
            self.camera_label.config(text=f"Camera error: {str(e)[:50]}", fg="white", bg="#2c3e50")
            # Retry after 2 seconds
            self.after(2000, self.start_camera_feed)

    def update_camera_feed(self):
        """Update the camera feed display - called continuously."""
        try:
            # Import here to avoid circular imports - access the global cap variable
            import inputs.distance as distance_module

            # Get the camera instance
            cap = distance_module.cap

            if cap is not None and cap.isOpened():
                # Read a fresh frame from the camera
                ret, frame = cap.read()

                if ret and frame is not None and frame.size > 0:
                    # Resize frame to fit display (maintain aspect ratio)
                    height, width = frame.shape[:2]
                    display_width = 320
                    display_height = 240

                    # Resize maintaining aspect ratio
                    frame = cv2.resize(frame, (display_width, display_height))

                    # Mirror the image horizontally (like a mirror)
                    frame = cv2.flip(frame, 1)

                    # Convert BGR to RGB for display
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Convert to PIL Image and then to PhotoImage
                    img = Image.fromarray(rgb_frame)
                    imgtk = ImageTk.PhotoImage(image=img)

                    # Update label with new image
                    self.camera_label.config(image=imgtk, text="", bg="#000000")
                    self.camera_label.image = imgtk  # Keep a reference to prevent garbage collection
                    # Reset error flag on successful read
                    self._camera_error_shown = False
                else:
                    # Only show error message if we haven't shown it recently
                    if not self._camera_error_shown:
                        self.camera_label.config(text="Camera read failed", fg="white", bg="#2c3e50")
                        self._camera_error_shown = True
            else:
                # Camera not initialized - try to reinitialize
                if not self._camera_error_shown:
                    self.camera_label.config(text="Initializing camera...", fg="white", bg="#2c3e50")
                    self._camera_error_shown = True
                # Try to initialize camera
                try:
                    from inputs.distance import initialize_camera
                    initialize_camera()
                except:
                    pass
        except Exception as e:
            # Only show error once
            if not self._camera_error_shown:
                try:
                    self.camera_label.config(text=f"Camera error", fg="white", bg="#2c3e50")
                    self._camera_error_shown = True
                except:
                    pass

        # Always schedule next update - continue updating even if there's an error
        # This ensures the feed keeps trying to update
        self.after(50, self.update_camera_feed)  # Update every 50ms for smoother feed (20 fps)
    
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
        self.camera_updating = False
        from core.controller import shutdown
        shutdown()
        self.destroy()


if __name__ == "__main__":
    # Test dashboard
    app = Dashboard()
    app.mainloop()

