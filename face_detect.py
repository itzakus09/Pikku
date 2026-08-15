import cv2

face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    h, w, _ = frame.shape
    center_x = w // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.3, 5)

    direction = "SEARCHING"
    action = "STOP"

    if len(faces) == 0:
        direction = "NO FACE"
        action = "STOP"

    for (x, y, fw, fh) in faces:
        face_center = x + fw // 2

        if face_center < center_x - 40:
            direction = "LEFT"
            action = "TURN LEFT"
        elif face_center > center_x + 40:
            direction = "RIGHT"
            action = "TURN RIGHT"
        else:
            direction = "CENTER"
            action = "MOVE FORWARD"

        cv2.rectangle(frame, (x,y), (x+fw,y+fh), (0,255,0), 2)

    cv2.putText(frame, direction, (w//3, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0,0,255), 4)

    cv2.putText(frame, action, (w//3, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,0,0), 3)

    cv2.line(frame, (center_x,0), (center_x,h), (255,0,0), 2)

    cv2.imshow("Robot Vision", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()