"""
Digital Skin Exposure Monitor - Main Entry Point
AI-Driven Approach to Track Blue Light and Thermal Exposure Effects on Skin Health

Research Project: 19APC4098
Student: M.Z.F.Zulfa
Supervisor: H.M.K.T.Gunewardhana

This system monitors:
- Distance from screen (using computer vision)
- Screen brightness (OS-level detection)
- Blue light exposure score (research-based formula)
- Thermal exposure score (proximity-based model)
"""

import tkinter as tk
import sys
import traceback
from ui.dashboard import Dashboard
from core.controller import monitor, initialize_session, shutdown


def update_system(dashboard):
    """
    Update the monitoring system and dashboard.
    This function is called periodically to refresh metrics.
    """
    try:
        # Get current monitoring interval
        from core.controller import get_monitoring_interval
        interval_ms = get_monitoring_interval() * 1000  # Convert to milliseconds
        
        # Perform monitoring cycle
        data = monitor()
        
        # Update dashboard with new data
        dashboard.update_metrics(data)
        
        # Schedule next update using dynamic interval
        dashboard.after(interval_ms, update_system, dashboard)
        
    except Exception as e:
        print(f"Error in update cycle: {e}")
        traceback.print_exc()
        # Continue monitoring even if one cycle fails
        from core.controller import get_monitoring_interval
        interval_ms = get_monitoring_interval() * 1000
        dashboard.after(interval_ms, update_system, dashboard)


def main():
    """Main application entry point."""
    try:
        # Initialize monitoring session
        print("Initializing Digital Skin Exposure Monitor...")
        initialize_session()
        print("Session initialized successfully.")
        
        # Create and configure dashboard
        print("Launching dashboard...")
        app = Dashboard()
        
        # Set up window close handler
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Start monitoring cycle
        print("Starting monitoring system...")
        update_system(app)
        
        # Run GUI event loop
        print("System ready. Monitoring active.")
        app.mainloop()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        shutdown()
        sys.exit(0)
        
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        shutdown()
        sys.exit(1)


if __name__ == "__main__":
    main()
