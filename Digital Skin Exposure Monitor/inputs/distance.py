"""
Distance Detection Module
Uses MediaPipe Face Mesh to calculate distance from webcam to user's face.
Based on inter-pupillary distance (IPD) measurement.
"""

import cv2
import mediapipe as mp
import math

# Physical constants
REAL_EYE_DISTANCE_CM = 6.3  # Average inter-pupillary distance in cm
FOCAL_LENGTH = 650  # Estimated focal length in pixels

# MediaPipe face mesh landmark indices for eyes
LEFT_EYE_INDEX = 133
RIGHT_EYE_INDEX = 362

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize webcam
cap = None

def initialize_camera():
    """Initialize the webcam."""
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Could not open webcam")
    return cap

def get_distance():
    """
    Calculate distance from webcam to face using face landmark detection.
    
    Returns:
        float: Distance in centimeters, or None if face not detected
    """
    global cap
    
    if cap is None:
        cap = initialize_camera()
    
    ret, frame = cap.read()
    if not ret:
        return None

    # Convert BGR to RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    # Check if face detected
    if not results.multi_face_landmarks:
        return None

    # Get face landmarks
    landmarks = results.multi_face_landmarks[0].landmark
    h, w, _ = frame.shape

    # Get eye coordinates
    x1 = int(landmarks[LEFT_EYE_INDEX].x * w)
    y1 = int(landmarks[LEFT_EYE_INDEX].y * h)
    x2 = int(landmarks[RIGHT_EYE_INDEX].x * w)
    y2 = int(landmarks[RIGHT_EYE_INDEX].y * h)

    # Calculate pixel distance between eyes
    pixel_dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    if pixel_dist == 0:
        return None

    # Calculate distance using focal length formula: distance = (real_size * focal_length) / pixel_size
    distance_cm = (REAL_EYE_DISTANCE_CM * FOCAL_LENGTH) / pixel_dist
    
    return round(distance_cm, 2)

def release_camera():
    """Release the webcam resource."""
    global cap
    if cap is not None:
        cap.release()
        cap = None

