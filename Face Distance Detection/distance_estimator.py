import cv2
import mediapipe as mp
import math

# ====== CONSTANTS ======
REAL_EYE_DISTANCE_CM = 6.3   # Average IPD
FOCAL_LENGTH = 650           # 🔴 Replace after calibration

LEFT_EYE_INDEX = 133
RIGHT_EYE_INDEX = 362

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)


def estimate_distance(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return None, None

    landmarks = results.multi_face_landmarks[0].landmark
    h, w, _ = frame.shape

    left_eye = landmarks[LEFT_EYE_INDEX]
    right_eye = landmarks[RIGHT_EYE_INDEX]

    x1, y1 = int(left_eye.x * w), int(left_eye.y * h)
    x2, y2 = int(right_eye.x * w), int(right_eye.y * h)

    pixel_distance = math.dist((x1, y1), (x2, y2))

    if pixel_distance == 0:
        return None, None

    distance_cm = (REAL_EYE_DISTANCE_CM * FOCAL_LENGTH) / pixel_distance

    return round(distance_cm, 2), round(pixel_distance, 2)
