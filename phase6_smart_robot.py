import cv2
import speech_recognition as sr
import pyttsx3
import threading

# ========== VOICE SETUP ==========
engine = pyttsx3.init()
engine.setProperty('rate', 160)

last_voice_cmd = "none"

def speak(text):
    print("ROBOT:", text)
    engine.say(text)
    engine.runAndWait()

def voice_thread():
    global last_voice_cmd
    r = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)

            cmd = r.recognize_google(audio).lower()
            print("VOICE:", cmd)

            if "stop" in cmd:
                last_voice_cmd = "stop"
                speak("Stopping")

        except:
            pass

# ========== CAMERA SETUP ==========
face = cv2.CascadeClassifier(cv2.data.haarcascades +
                             "haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)

# Start voice thread
threading.Thread(target=voice_thread, daemon=True).start()

speak("Smart robot activated")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    h, w, _ = frame.shape
    center_x = w // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.3, 5)

    action = "STOP"

    if len(faces) > 0:
        x, y, fw, fh = faces[0]
        face_center = x + fw // 2

        if face_center < center_x - 40:
            action = "TURN LEFT"
        elif face_center > center_x + 40:
            action = "TURN RIGHT"
        else:
            action = "MOVE FORWARD"

        cv2.rectangle(frame, (x,y), (x+fw, y+fh), (0,255,0), 2)

    # Voice override
    if last_voice_cmd == "stop":
        action = "STOP"

    print("ROBOT:", action)

    cv2.line(frame, (center_x,0), (center_x,h), (255,0,0), 2)
    cv2.putText(frame, action, (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("PHASE 6 - Smart Robot Brain", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()