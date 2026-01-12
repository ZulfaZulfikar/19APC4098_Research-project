"""
Thermal Exposure Module
Calculates thermal exposure score based on proximity to screen and exposure duration.
Based on research on erythema ab igne (toasted skin syndrome) from device heat.
"""


def thermal_score(duration_min, distance_cm):
    """
    Calculate thermal exposure score.
    
    Formula: Score = (Duration / Distance) × M
    Where M is a calibration constant based on thermal exposure research.
    
    Closer proximity and longer duration increase thermal risk.
    
    Args:
        duration_min (int): Exposure duration in minutes
        distance_cm (float): Distance from screen in centimeters
        
    Returns:
        float: Thermal exposure score (0-100)
    """
    if not distance_cm or distance_cm <= 0:
        return 0.0

    # Calibration constant (M) based on thermal exposure literature
    # Adjusted to normalize scores to 0-100 range
    M = 1.5
    
    # Closer distance and longer duration increase thermal exposure
    score = (duration_min / distance_cm) * M

    # Cap score at 100
    return min(100, round(score, 2))


def thermal_risk(score):
    """
    Classify thermal exposure risk level based on score.
    
    Args:
        score (float): Thermal exposure score
        
    Returns:
        str: Risk level ("LOW", "MODERATE", or "HIGH")
    """
    if score <= 30:
        return "LOW"
    elif score <= 70:
        return "MODERATE"
    else:
        return "HIGH"


def get_thermal_recommendations(risk_level):
    """
    Get recommendations based on thermal risk level.
    
    Args:
        risk_level (str): Risk level ("LOW", "MODERATE", or "HIGH")
        
    Returns:
        str: Recommendation message
    """
    recommendations = {
        "LOW": "Thermal exposure is minimal. Maintain safe distance.",
        "MODERATE": "You are getting closer to the screen. Increase distance to reduce thermal exposure.",
        "HIGH": "You are too close to the screen. Move further away immediately to prevent thermal skin damage."
    }
    return recommendations.get(risk_level, "Monitor your distance from the screen.")

