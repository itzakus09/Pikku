import cv2
import speech_recognition as sr
import threading
import pygame
import sys

# ------------------ VOICE CONTROL ------------------

voice_command = "NONE"

def listen_voice():
    global voice_command
    r = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        try:
            with mic as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=3)

            text = r.recognize_google(audio).lower()
            print("You said:", text)

            if "stop" in text:
                voice_command = "STOP"
            elif "forward" in text:
                voice_command = "FORWARD"
            elif "left" in text:
                voice_command = "LEFT"
            elif "right" in text:
                voice_command = "RIGHT"
            else:
                voice_command = "NONE"

        except:
            voice_command = "NONE"

# ------------------ CAMERA SETUP ------------------

face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)

# ------------------ ROBOT SIMULATOR ------------------

pygame.init()
W, H = 500, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("PHASE 5 - AI Robot Simulator")

x, y = 250, 250
speed = 5

# ------------------ START VOICE THREAD ------------------

voice_thread = threading.Thread(target=listen_voice, daemon=True)
voice_thread.start()

# ------------------ MAIN LOOP ------------------

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cam.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

    ret, frame = cam.read()
    if not ret:
        break

    h, w, _ = frame.shape
    center_x = w // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.3, 5)

    direction = "STOP"

    if len(faces) > 0:
        (fx, fy, fw, fh) = faces[0]
        face_center = fx + fw // 2

        if face_center < center_x - 40:
            direction = "LEFT"
        elif face_center > center_x + 40:
            direction = "RIGHT"
        else:
            direction = "CENTER"

        cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), (0,255,0), 2)

    # ------------------ DECISION BRAIN ------------------

    action = direction

    if voice_command == "STOP":
        action = "STOP"
    elif voice_command != "NONE":
        action = voice_command

    # ------------------ ROBOT MOVE ------------------

    if action == "FORWARD" or action == "CENTER":
        y -= speed
    elif action == "LEFT":
        x -= speed
    elif action == "RIGHT":
        x += speed

    # ------------------ DRAW ROBOT ------------------

    screen.fill((230,230,230))
    pygame.draw.rect(screen, (0,0,255), (x, y, 30, 30))
    pygame.display.update()

    # ------------------ CAMERA DISPLAY ------------------

    cv2.line(frame, (center_x,0), (center_x,h), (255,0,0), 2)

    cv2.putText(frame, f"FACE DIR: {direction}", (20,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    cv2.putText(frame, f"VOICE: {voice_command}", (20,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    cv2.putText(frame, f"ACTION: {action}", (20,90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,150,0), 2)

    cv2.imshow("AI Robot Vision", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
pygame.quit()