"""
Core Controller Module
Orchestrates the monitoring system, calculates exposure scores, logs data, and triggers alerts.
"""

import time
import csv
import os
from datetime import datetime

from inputs.distance import get_distance, initialize_camera, release_camera
from inputs.brightness import get_brightness
from exposure.blue_light import blue_light_score, blue_light_risk, get_blue_light_recommendations
from exposure.thermal import thermal_score, thermal_risk, get_thermal_recommendations
from ui.alert_popup import show_alert

# Configuration
LOG_FILE = "data/exposure_log.csv"
MONITORING_INTERVAL = 5  # seconds between monitoring cycles (can be updated via settings)
ALERT_COOLDOWN = 300  # seconds between same alert type (5 minutes, can be updated via settings)

def get_monitoring_interval():
    """Get current monitoring interval."""
    return MONITORING_INTERVAL

def get_alert_cooldown():
    """Get current alert cooldown."""
    return ALERT_COOLDOWN

def set_monitoring_interval(seconds):
    """Set monitoring interval."""
    global MONITORING_INTERVAL
    MONITORING_INTERVAL = max(1, int(seconds))  # Minimum 1 second

def set_alert_cooldown(seconds):
    """Set alert cooldown."""
    global ALERT_COOLDOWN
    ALERT_COOLDOWN = max(0, int(seconds))  # Minimum 0 seconds

# Global state
session_start_time = None
last_blue_alert_time = 0
last_thermal_alert_time = 0


def initialize_session():
    """Initialize a new monitoring session."""
    global session_start_time
    session_start_time = time.time()
    
    # Initialize camera
    try:
        initialize_camera()
    except Exception as e:
        print(f"Camera initialization error: {e}")
    
    # Initialize CSV log file if it doesn't exist
    if not os.path.exists(LOG_FILE):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "DateTime",
                "Distance_cm",
                "Brightness",
                "BlueLightScore",
                "ThermalScore",
                "BlueRisk",
                "ThermalRisk"
            ])


def get_session_duration_minutes():
    """Get current session duration in minutes."""
    global session_start_time
    if session_start_time is None:
        return 0
    return int((time.time() - session_start_time) / 60)


def monitor():
    """
    Perform one monitoring cycle: collect data, calculate scores, log, and check alerts.
    
    Returns:
        dict: Monitoring data with all metrics
    """
    global last_blue_alert_time, last_thermal_alert_time
    
    # Get current metrics
    duration_min = get_session_duration_minutes()
    distance = get_distance()
    brightness = get_brightness()
    
    # Default brightness to 60 if None (for macOS and other systems where detection might fail)
    if brightness is None:
        brightness = 60

    # Calculate exposure scores
    # Always calculate even if brightness is 0 or None (the function handles it)
    blue_score = blue_light_score(brightness, duration_min, distance) if distance else 0.0
    thermal_score_val = thermal_score(duration_min, distance) if distance else 0.0

    # Determine risk levels
    blue_risk = blue_light_risk(blue_score)
    thermal_risk_val = thermal_risk(thermal_score_val)

    # Log data
    log_data(distance, brightness, blue_score, thermal_score_val, blue_risk, thermal_risk_val)

    # Check for alerts (with cooldown to prevent spam)
    current_time = time.time()
    
    if blue_risk == "HIGH" and (current_time - last_blue_alert_time) > ALERT_COOLDOWN:
        show_alert(
            "High Blue Light Exposure",
            get_blue_light_recommendations(blue_risk)
        )
        last_blue_alert_time = current_time

    if thermal_risk_val == "HIGH" and (current_time - last_thermal_alert_time) > ALERT_COOLDOWN:
        show_alert(
            "High Thermal Exposure",
            get_thermal_recommendations(thermal_risk_val)
        )
        last_thermal_alert_time = current_time

    # Return monitoring data
    return {
        "distance": distance,
        "brightness": brightness,
        "blue_score": blue_score,
        "thermal_score": thermal_score_val,
        "blue_risk": blue_risk,
        "thermal_risk": thermal_risk_val,
        "duration_min": duration_min
    }


def log_data(distance, brightness, blue_score, thermal_score, blue_risk, thermal_risk):
    """
    Log monitoring data to CSV file.
    
    Args:
        distance: Distance in cm
        brightness: Brightness percentage
        blue_score: Blue light exposure score
        thermal_score: Thermal exposure score
        blue_risk: Blue light risk level
        thermal_risk: Thermal risk level
    """
    try:
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                distance if distance else "N/A",
                brightness if brightness else "N/A",
                blue_score,
                thermal_score,
                blue_risk,
                thermal_risk
            ])
    except Exception as e:
        print(f"Error logging data: {e}")


def reset_session():
    """Reset the monitoring session."""
    global session_start_time, last_blue_alert_time, last_thermal_alert_time
    session_start_time = time.time()
    last_blue_alert_time = 0
    last_thermal_alert_time = 0


def shutdown():
    """Cleanup resources on shutdown."""
    release_camera()

