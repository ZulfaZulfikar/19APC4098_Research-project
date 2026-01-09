import tkinter as tk
from tkinter import ttk
from alert_popup import show_alert
from history import HistoryWindow
from settings import SettingsWindow

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Digital Skin Exposure Monitor")
        self.geometry("900x620")
        # Change: Deep navy-blue background
        self.configure(bg="#0f172a")
        self.resizable(False, False)

        self.create_header()
        self.create_live_metrics()
        self.create_exposure_scores()
        self.create_recommendation()
        self.create_footer()

    def create_header(self):
        # Change: Darker slate header
        header = tk.Frame(self, bg="#1e293b", height=55)
        header.pack(fill="x")

        tk.Label(
            header, text="Digital Skin Exposure Monitor",
            fg="#f8fafc", bg="#1e293b",
            font=("Segoe UI", 15, "bold")
        ).pack(side="left", padx=20)

        tk.Label(
            header, text="● Monitoring ON",
            fg="#4ade80", bg="#1e293b", # Change: Mint green
            font=("Segoe UI", 11, "bold")
        ).pack(side="right", padx=20)

    def create_live_metrics(self):
        # Change: Slate blue box with cyan labels
        box = tk.LabelFrame(self, text="Live Metrics", padx=15, pady=10, bg="#1e293b", fg="#94a3b8")
        box.pack(fill="x", padx=20, pady=10)

        metrics = [
            ("Face-to-Screen Distance:", "52 cm"),
            ("Screen Brightness:", "78 %"),
            ("Session Duration:", "1h 25m"),
            ("Today's Screen Time:", "6h 10m"),
        ]

        for i, (k, v) in enumerate(metrics):
            tk.Label(box, text=k, bg="#1e293b", fg="#cbd5e1").grid(row=i, column=0, sticky="w", pady=3)
            # Change: Value labels now use Cyan (#38bdf8)
            tk.Label(box, text=v, font=("Segoe UI", 10, "bold"), bg="#1e293b", fg="#38bdf8").grid(row=i, column=1, padx=10)

    def create_exposure_scores(self):
        box = tk.LabelFrame(self, text="Exposure Risk Scores", padx=15, pady=10, bg="#1e293b", fg="#94a3b8")
        box.pack(fill="x", padx=20)

        tk.Label(box, text="Blue Light Exposure", bg="#1e293b", fg="#f8fafc").pack(anchor="w")
        self.blue_bar = ttk.Progressbar(box, length=700, maximum=100, value=62)
        self.blue_bar.pack(pady=4)
        # Change: Vivid Amber for Warning
        tk.Label(box, text="Risk: MODERATE", fg="#fbbf24", bg="#1e293b", font=("Segoe UI", 9, "bold")).pack(anchor="w")

        tk.Label(box, text="Thermal Exposure", bg="#1e293b", fg="#f8fafc").pack(anchor="w", pady=(8, 0))
        self.thermal_bar = ttk.Progressbar(box, length=700, maximum=100, value=45)
        self.thermal_bar.pack(pady=4)
        tk.Label(box, text="Risk: MODERATE", fg="#fbbf24", bg="#1e293b", font=("Segoe UI", 9, "bold")).pack(anchor="w")

    def create_recommendation(self):
        box = tk.LabelFrame(self, text="Live Recommendation", padx=15, pady=10, bg="#1e293b", fg="#94a3b8")
        box.pack(fill="x", padx=20, pady=10)

        self.recommendation = tk.Label(
            box,
            text="Consider increasing distance to 60 cm",
            fg="#f87171", font=("Segoe UI", 11, "bold"), bg="#1e293b" # Change: Soft red alert
        )
        self.recommendation.pack(anchor="w")

        self.after(2000, lambda: show_alert("Increase screen distance to reduce exposure"))

    def create_footer(self):
        footer = tk.Frame(self, bg="#1e293b", height=60)  # Increased height slightly for breathing room
        footer.pack(fill="x", side="bottom")

        # Buttons will now automatically use the "TButton" style defined above
        ttk.Button(footer, text="View History", command=HistoryWindow).pack(side="left", padx=20, pady=15)
        ttk.Button(footer, text="Settings", command=SettingsWindow).pack(side="left")
        ttk.Button(footer, text="Pause Monitoring").pack(side="right", padx=20)