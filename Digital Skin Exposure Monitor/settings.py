import tkinter as tk

class SettingsWindow:
    def __init__(self):
        win = tk.Toplevel()
        win.title("Settings")
        win.geometry("400x300")

        tk.Label(win, text="Settings", font=("Segoe UI", 14, "bold")).pack(pady=10)

        tk.Checkbutton(win, text="Enable Notifications").pack(anchor="w", padx=20)
        tk.Checkbutton(win, text="Auto Brightness Alerts").pack(anchor="w", padx=20)

        tk.Label(win, text="Alert Distance (cm)").pack(anchor="w", padx=20, pady=(10, 0))
        tk.Scale(win, from_=30, to=80, orient="horizontal").pack(padx=20)

        tk.Button(win, text="Save Settings").pack(pady=20)
