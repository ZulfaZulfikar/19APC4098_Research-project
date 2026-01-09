import cv2
from distance_estimator import estimate_distance

def main():
    cap = cv2.VideoCapture(0)

    print("Webcam started")
    print("Press 'Q' to exit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        distance, pixel_dist = estimate_distance(frame)

        if distance:
            cv2.putText(frame, f"Distance: {distance} cm",
                        (30, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 255, 0), 2)

        cv2.imshow("Face Distance Estimation", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# 🔥 THIS is the Python "main method"
if __name__ == "__main__":
    main()
