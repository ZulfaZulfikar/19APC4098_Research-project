"""
Alert Popup Module
Displays alert notifications when high exposure is detected.
"""

import tkinter as tk
from tkinter import messagebox


def show_alert(title, message):
    """
    Display an alert popup.
    
    Args:
        title (str): Alert title
        message (str): Alert message
    """
    # Use messagebox for cross-platform alerts
    root = tk.Tk()
    root.withdraw()  # Hide main window
    messagebox.showwarning(title, message)
    root.destroy()


def show_info(title, message):
    """
    Display an info popup.
    
    Args:
        title (str): Info title
        message (str): Info message
    """
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()

