import cv2
import numpy as np

# Load face model
face = cv2.CascadeClassifier(cv2.data.haarcascades +
                             "haarcascade_frontalface_default.xml")

cam = cv2.VideoCapture(0)

# Virtual servo angle
servo_angle = 90   # start center

while True:
    ret, frame = cam.read()
    if not ret:
        break

    h, w, _ = frame.shape
    center_x = w // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.3, 5)

    direction = "NO FACE"

    for (x, y, fw, fh) in faces:
        face_center = x + fw // 2

        # Direction logic
        if face_center < center_x - 40:
            direction = "LEFT"
            servo_angle -= 2
        elif face_center > center_x + 40:
            direction = "RIGHT"
            servo_angle += 2
        else:
            direction = "CENTER"

        # Limit servo angle
        servo_angle = max(0, min(180, servo_angle))

        # Draw face box
        cv2.rectangle(frame, (x, y), (x+fw, y+fh), (0,255,0), 2)
        break

    # Draw center line
    cv2.line(frame, (center_x, 0), (center_x, h), (255,0,0), 2)

    # Show direction
    cv2.putText(frame, f"DIR: {direction}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # Show servo angle
    cv2.putText(frame, f"HEAD ANGLE: {servo_angle} deg", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

    cv2.imshow("PHASE 2 - Head Tracking", frame)

    if cv2.waitKey(1) == 27:  # ESC
        break

cam.release()
cv2.destroyAllWindows()
