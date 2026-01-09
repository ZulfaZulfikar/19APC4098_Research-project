import tkinter as tk

def show_alert(message):
    popup = tk.Toplevel()
    popup.title("Exposure Alert")
    popup.geometry("350x150")
    popup.resizable(False, False)

    tk.Label(
        popup, text="⚠ Exposure Warning",
        font=("Segoe UI", 13, "bold"), fg="red"
    ).pack(pady=10)

    tk.Label(
        popup, text=message,
        font=("Segoe UI", 11)
    ).pack(pady=10)

    tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)
