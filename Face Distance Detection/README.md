# Webcam-Based Face Distance Estimation

This project estimates the distance between a user and a laptop screen using a webcam.

## Method
- MediaPipe Face Mesh for eye landmark detection
- Inter-pupillary distance (IPD) based geometry
- Inverse proportional relationship between pixel distance and real distance

## Formula
Distance (cm) = (Real Eye Distance × Focal Length) / Eye Pixel Distance

## Accuracy
±5–10% depending on lighting and camera quality.

## Usage
   pip install opencv-python mediapipe numpy pandas screen-brightness-control

1. Run main.py to view live distance
2. Calibrate once using calibration.py
3. Update focal length in distance_estimator.py
