"""
Blue Light Exposure Module
Calculates blue light exposure score based on screen brightness, duration, and distance.
Based on research literature on blue light effects on skin health.
"""


def blue_light_score(brightness, duration_min, distance_cm):
    """
    Calculate blue light exposure score.
    
    Formula: Score = (Brightness × Duration) / (Distance²) × K
    Where K is a calibration constant based on literature research.
    
    Args:
        brightness (int): Screen brightness percentage (0-100)
        duration_min (int): Exposure duration in minutes
        distance_cm (float): Distance from screen in centimeters
        
    Returns:
        float: Blue light exposure score (0-100)
    """
    if not brightness or not distance_cm or distance_cm <= 0:
        return 0.0

    # Calibration constant (K) based on research literature
    # Adjusted to normalize scores to 0-100 range
    K = 0.02
    
    # Inverse square law: exposure decreases with distance squared
    # Higher brightness and longer duration increase exposure
    score = ((brightness * duration_min) / (distance_cm ** 2)) * K

    # Cap score at 100
    return min(100, round(score, 2))


def blue_light_risk(score):
    """
    Classify blue light exposure risk level based on score.
    
    Args:
        score (float): Blue light exposure score
        
    Returns:
        str: Risk level ("LOW", "MODERATE", or "HIGH")
    """
    if score <= 30:
        return "LOW"
    elif score <= 70:
        return "MODERATE"
    else:
        return "HIGH"


def get_blue_light_recommendations(risk_level):
    """
    Get recommendations based on blue light risk level.
    
    Args:
        risk_level (str): Risk level ("LOW", "MODERATE", or "HIGH")
        
    Returns:
        str: Recommendation message
    """
    recommendations = {
        "LOW": "Blue light exposure is within safe limits. Continue current usage.",
        "MODERATE": "Consider reducing screen brightness or taking periodic breaks.",
        "HIGH": "High blue light exposure detected. Reduce brightness, increase distance, or take a break immediately."
    }
    return recommendations.get(risk_level, "Monitor your exposure levels.")

