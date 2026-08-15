import cv2

# Load face model
face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cam = cv2.VideoCapture(0)

SERVO_MIN = 30
SERVO_MAX = 150

def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    h, w, _ = frame.shape
    center_x = w // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.3, 5)

    servo_angle = 90
    direction = "NO FACE"

    for (x, y, fw, fh) in faces:
        face_center = x + fw // 2

        servo_angle = map_value(face_center, 0, w, SERVO_MIN, SERVO_MAX)

        if face_center < center_x - 40:
            direction = "HEAD LEFT"
        elif face_center > center_x + 40:
            direction = "HEAD RIGHT"
        else:
            direction = "HEAD CENTER"

        cv2.rectangle(frame, (x,y), (x+fw, y+fh), (0,255,0), 2)
        break

    # center line
    cv2.line(frame, (center_x, 0), (center_x, h), (255,0,0), 2)

    cv2.putText(frame, f"DIR: {direction}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.putText(frame, f"SERVO ANGLE: {servo_angle} deg", (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.imshow("PHASE 4 - Head Servo Tracking", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()