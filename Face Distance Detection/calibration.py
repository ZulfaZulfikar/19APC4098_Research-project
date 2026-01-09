# calibration.py
# Calculate camera focal length for accurate distance estimation

KNOWN_DISTANCE_CM = 50       # Change if needed
REAL_EYE_DISTANCE_CM = 6.3   # Average human IPD

pixel_eye_distance = float(input("Enter eye pixel distance from webcam frame: "))

focal_length = (pixel_eye_distance * KNOWN_DISTANCE_CM) / REAL_EYE_DISTANCE_CM

print("\n✅ Calibration Complete")
print("Save this FOCAL_LENGTH value:")
print(f"FOCAL_LENGTH = {round(focal_length, 2)}")
